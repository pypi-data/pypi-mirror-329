# ----------------------------------------------------------------------------
# PyGMTSAR
# 
# This file is part of the PyGMTSAR project: https://github.com/mobigroup/gmtsar
# 
# Copyright (c) 2025, Alexey Pechnikov
# 
# Licensed under the BSD 3-Clause License (see LICENSE for details)
# ----------------------------------------------------------------------------
from .S1_geocode import S1_geocode

class S1_topo(S1_geocode):

    def get_topo(self, burst, trans_inv='auto'):
        """
        Get the radar topography grid.

        Returns
        -------
        xarray.DataArray
            The 'topo' variable data is a xarray.DataArray.

        Examples
        --------
        Get DEM:
        topo = stack.get_topo()

        Notes
        -----
        This method returns 'topo' variable from inverse radar transform grid.
        """
        if isinstance(trans_inv, str) and trans_inv == 'auto':
            trans_inv = self.get_trans_inv(burst)

        return trans_inv['ele'].rename('topo')

    def plot_topo(self, burst, data='auto', caption='Topography on WGS84 ellipsoid, [m]',
                  quantile=None, vmin=None, vmax=None, symmetrical=False,
                  cmap='gray', aspect=None, **kwargs):
        import numpy as np
        import matplotlib.pyplot as plt

        if isinstance(data, str) and data == 'auto':
            data = self.get_topo(burst)

        if quantile is not None:
            assert vmin is None and vmax is None, "ERROR: arguments 'quantile' and 'vmin', 'vmax' cannot be used together"

        if quantile is not None:
            vmin, vmax = np.nanquantile(data, quantile)

        # define symmetrical boundaries
        if symmetrical is True and vmax > 0:
            minmax = max(abs(vmin), vmax)
            vmin = -minmax
            vmax =  minmax

        plt.figure()
        data.plot.imshow(cmap=cmap, vmin=vmin, vmax=vmax)
        self.plot_AOI(**kwargs)
        self.plot_POI(**kwargs)
        if aspect is not None:
            plt.gca().set_aspect(aspect)
        plt.xlabel('Range')
        plt.ylabel('Azimuth')
        plt.title(caption)

    def topo_phase(self, burst, dates=None, topo='auto', grid=None, method='nearest', debug=False):
        """
        np.arctan2(np.sin(topo_phase), np.cos(topo_phase))[0].plot.imshow()
        """
        import pandas as pd
        import dask
        import dask.array as da
        import xarray as xr
        import numpy as np
        import joblib
        import warnings
        # suppress Dask warning "RuntimeWarning: invalid value encountered in divide"
        warnings.filterwarnings('ignore')
        warnings.filterwarnings('ignore', module='dask')
        warnings.filterwarnings('ignore', module='dask.core')

        if debug:
            print ('DEBUG: topo_phase')

        if dates is None:
            dates = self.df.index.get_level_values(1).unique()

        if isinstance(topo, str) and topo == 'auto':
            topo = self.get_topo(burst)

        # calculate the combined earth curvature and topography correction
        def calc_drho(rho, topo, earth_radius, height, b, alpha, Bx):
            sina = np.sin(alpha)
            cosa = np.cos(alpha)
            c = earth_radius + height
            # compute the look angle using equation (C26) in Appendix C
            # GMTSAR uses long double here
            #ret = earth_radius + topo.astype(np.longdouble)
            ret = earth_radius + topo
            cost = ((rho**2 + c**2 - ret**2) / (2. * rho * c))
            #if (cost >= 1.)
            #    die("calc_drho", "cost >= 0");
            sint = np.sqrt(1. - cost**2)
            # Compute the offset effect from non-parallel orbit
            term1 = rho**2 + b**2 - 2 * rho * b * (sint * cosa - cost * sina) - Bx**2
            drho = -rho + np.sqrt(term1)
            del term1, sint, cost, ret, c, cosa, sina
            return drho
            
        #def block_phase(prm1, prm2, ylim, xlim):
        def block_phase_dask(block_topo, y_chunk, x_chunk, prm1, prm2):
            from scipy import constants

            if prm1 is None or prm2 is None:
                return np.ones_like(block_topo).astype(np.complex64)

            # get full dimensions
            xdim = prm1.get('num_rng_bins')
            ydim = prm1.get('num_patches') * prm1.get('num_valid_az')

            # get heights
            htc = prm1.get('SC_height')
            ht0 = prm1.get('SC_height_start')
            htf = prm1.get('SC_height_end')

            # compute the time span and the time spacing
            tspan = 86400 * abs(prm2.get('SC_clock_stop') - prm2.get('SC_clock_start'))
            assert (tspan >= 0.01) and (prm2.get('PRF') >= 0.01), \
                f"ERROR in sc_clock_start={prm2.get('SC_clock_start')}, sc_clock_stop={prm2.get('SC_clock_stop')}, or PRF={prm2.get('PRF')}"

            # setup the default parameters
            drange = constants.speed_of_light / (2 * prm2.get('rng_samp_rate'))
            alpha = prm2.get('alpha_start') * np.pi / 180
            # a constant that converts drho into a phase shift
            cnst = -4 * np.pi / prm2.get('radar_wavelength')

            # calculate initial baselines
            Bh0 = prm2.get('baseline_start') * np.cos(prm2.get('alpha_start') * np.pi / 180)
            Bv0 = prm2.get('baseline_start') * np.sin(prm2.get('alpha_start') * np.pi / 180)
            Bhf = prm2.get('baseline_end')   * np.cos(prm2.get('alpha_end')   * np.pi / 180)
            Bvf = prm2.get('baseline_end')   * np.sin(prm2.get('alpha_end')   * np.pi / 180)
            Bx0 = prm2.get('B_offset_start')
            Bxf = prm2.get('B_offset_end')

            # first case is quadratic baseline model, second case is default linear model
            if prm2.get('baseline_center') != 0 or prm2.get('alpha_center') != 0 or prm2.get('B_offset_center') != 0:
                Bhc = prm2.get('baseline_center') * np.cos(prm2.get('alpha_center') * np.pi / 180)
                Bvc = prm2.get('baseline_center') * np.sin(prm2.get('alpha_center') * np.pi / 180)
                Bxc = prm2.get('B_offset_center')

                dBh = (-3 * Bh0 + 4 * Bhc - Bhf) / tspan
                dBv = (-3 * Bv0 + 4 * Bvc - Bvf) / tspan
                ddBh = (2 * Bh0 - 4 * Bhc + 2 * Bhf) / (tspan * tspan)
                ddBv = (2 * Bv0 - 4 * Bvc + 2 * Bvf) / (tspan * tspan)

                dBx = (-3 * Bx0 + 4 * Bxc - Bxf) / tspan
                ddBx = (2 * Bx0 - 4 * Bxc + 2 * Bxf) / (tspan * tspan)
            else:
                dBh = (Bhf - Bh0) / tspan
                dBv = (Bvf - Bv0) / tspan
                dBx = (Bxf - Bx0) / tspan
                ddBh = ddBv = ddBx = 0

            # calculate height increment
            dht = (-3 * ht0 + 4 * htc - htf) / tspan
            ddht = (2 * ht0 - 4 * htc + 2 * htf) / (tspan * tspan)

            near_range = (prm1.get('near_range') + \
                x_chunk.reshape(1,-1) * (1 + prm1.get('stretch_r')) * drange) + \
                y_chunk.reshape(-1,1) * prm1.get('a_stretch_r') * drange

            # calculate the change in baseline and height along the frame
            time = y_chunk * tspan / (ydim - 1)        
            Bh = Bh0 + dBh * time + ddBh * time**2
            Bv = Bv0 + dBv * time + ddBv * time**2
            Bx = Bx0 + dBx * time + ddBx * time**2
            B = np.sqrt(Bh * Bh + Bv * Bv)
            alpha = np.arctan2(Bv, Bh)
            height = ht0 + dht * time + ddht * time**2

            # calculate the combined earth curvature and topography correction
            drho = calc_drho(near_range, block_topo, prm1.get('earth_radius'),
                             height.reshape(-1, 1), B.reshape(-1, 1), alpha.reshape(-1, 1), Bx.reshape(-1, 1))

            #phase_shift = np.exp(1j * (cnst * drho))
            phase_shift = cnst * drho
            del near_range, drho, height, B, alpha, Bx, Bv, Bh, time

            # for 3d processing
            #return np.expand_dims(phase_shift.astype(np.complex64), 0)
            #return phase_shift.astype(np.complex64)
            return phase_shift.astype(np.float32)

        def prepare_prms(burst, date):
            if date == self.reference:
                return (None, None)
            prm1 = self.PRM(burst)
            prm2 = self.PRM(burst, date)
            prm2.set(prm1.SAT_baseline(prm2, tail=9)).fix_aligned()
            prm1.set(prm1.SAT_baseline(prm1).sel('SC_height','SC_height_start','SC_height_end')).fix_aligned()
            return (prm1, prm2)

        prms = joblib.Parallel(n_jobs=-1)(joblib.delayed(prepare_prms)(burst, date) for date in dates)

        # fill NaNs by 0 and expand to 3d
        topo2d = da.where(da.isnan(topo.data), 0, topo.data)

        # for 3d processing
        # topo3d = da.repeat(da.expand_dims(topo2d, 0), len(pairs), axis=0).rechunk((1, 'auto', 'auto'))
        # out = da.blockwise(
        #     block_phase_dask,
        #     'kyx',
        #     topo3d, 'kyx',
        #     topo.y,    'y',
        #     topo.x,    'x',
        #     [prm[0] for prm in prms], 'k',
        #     [prm[1] for prm in prms], 'k',
        #     dtype=np.complex64,
        # )

        out = da.stack([da.blockwise(
            block_phase_dask,
            'yx',
            topo2d, 'yx',
            topo.a, 'y',
            topo.r, 'x',
            prm1=prm[0],
            prm2=prm[1],
            #dtype=np.complex64
            dtype=np.float32
        ) for prm in prms], axis=0)

        coords = coords={'date': pd.to_datetime(dates), 'a': topo.a, 'r': topo.r}
        return xr.DataArray(out, coords).where(da.isfinite(topo)).rename('phase')

