# ----------------------------------------------------------------------------
# PyGMTSAR
# 
# This file is part of the PyGMTSAR project: https://github.com/mobigroup/gmtsar
# 
# Copyright (c) 2025, Alexey Pechnikov
# 
# Licensed under the BSD 3-Clause License (see LICENSE for details)
# ----------------------------------------------------------------------------
from .S1_dem import S1_dem
from .PRM import PRM

class S1_align(S1_dem):

    @staticmethod
    def _offset2shift(xyz, rmax, amax, method='linear'):
        """
        Convert offset coordinates to shift values on a grid.

        Parameters
        ----------
        xyz : numpy.ndarray
            Array containing the offset coordinates (x, y, z).
        rmax : int
            Maximum range bin.
        amax : int
            Maximum azimuth line.
        method : str, optional
            Interpolation method. Default is 'linear'.

        Returns
        -------
        xarray.DataArray
            Array containing the shift values on a grid.
        """
        import xarray as xr
        import numpy as np
        from scipy.interpolate import griddata

        # use center pixel GMT registration mode
        rngs = np.arange(8/2, rmax+8/2, 8)
        azis = np.arange(4/2, amax+4/2, 4)
        grid_r, grid_a = np.meshgrid(rngs, azis)

        # crashes in Docker containers on Türkiye Earthquakes for scipy=1.12.0
        grid = griddata((xyz[:,0], xyz[:,1]), xyz[:,2], (grid_r, grid_a), method=method)
        da = xr.DataArray(np.flipud(grid), coords={'y': azis, 'x': rngs}, name='z')
        return da

    # replacement for gmt grdfilter ../topo/dem.grd -D2 -Fg2 -I12s -Gflt.grd
    # use median decimation instead of average
    def _get_topo_llt(self, degrees, debug=False):
        """
        Get the topography coordinates (lon, lat, z) for decimated DEM.

        Parameters
        ----------
        degrees : float
            Number of degrees for decimation.
        debug : bool, optional
            Enable debug mode. Default is False.

        Returns
        -------
        numpy.ndarray
            Array containing the topography coordinates (lon, lat, z).
        """
        import xarray as xr
        import numpy as np
        import warnings
        # supress warnings "UserWarning: The specified chunks separate the stored chunks along dimension"
        warnings.filterwarnings('ignore')

        # add buffer around the cropped area for borders interpolation
        dem_area = self.get_dem()
        
        ny = int(np.round(degrees/dem_area.lat.diff('lat')[0]))
        nx = int(np.round(degrees/dem_area.lon.diff('lon')[0]))
        if debug:
            print ('DEBUG: DEM decimation','ny', ny, 'nx', nx)
        dem_area = dem_area.coarsen({'lat': ny, 'lon': nx}, boundary='pad').mean()

        lats, lons, z = xr.broadcast(dem_area.lat, dem_area.lon, dem_area)
        topo_llt = np.column_stack([lons.values.ravel(), lats.values.ravel(), z.values.ravel()])
        # filter out records where the third column (index 2) is NaN
        return topo_llt[~np.isnan(topo_llt[:, 2])]

    # aligning for reference image
    def _align_ref(self, burst, debug=False):
        """
        Align and stack the reference scene.

        Parameters
        ----------
        debug : bool, optional
            Enable debug mode. Default is False.

        Returns
        -------
        None

        Examples
        --------
        stack.stack_ref(debug=True)
        """
        import xarray as xr
        import numpy as np
        import os

        #reference_line = list(self.get_reference(burst).itertuples())[0]
        #print (reference_line)

        # for reference scene
        prefix = self.get_prefix(burst)
        path_prefix = os.path.join(self.basedir, prefix)

        # generate PRM, LED, SLC
        self._make_s1a_tops(burst, debug=debug)

        PRM.from_file(path_prefix + '.PRM')\
            .calc_dop_orb(inplace=True).update()

    # aligning for secondary image
    def _align_rep(self, burst, date=None, degrees=12.0/3600, debug=False):
        """
        Align and stack secondary images.

        Parameters
        ----------
        date : str or None, optional
            Date of the image to process. If None, process all images. Default is None.
        degrees : float, optional
            Degrees per pixel resolution for the coarse DEM. Default is 12.0/3600.
        debug : bool, optional
            Enable debug mode. Default is False.

        Returns
        -------
        None

        Examples
        --------
        stack.stack_rep(date='2023-05-01', degrees=15.0/3600, debug=True)
        """
        import xarray as xr
        import numpy as np
        import os
        
        # temporary filenames to be removed
        cleanup = []

        ref_prefix = self.get_prefix(burst)
        rep_prefix = self.get_prefix(burst, date)

        # define reference image parameters
        earth_radius = self.PRM(burst).get('earth_radius')

        # prepare coarse DEM for alignment
        # 12 arc seconds resolution is enough, for SRTM 90m decimation is 4x4
        topo_llt = self._get_topo_llt(degrees=degrees)
        #topo_llt.shape

        # define relative filenames for PRM
        rep_prm  = os.path.join(self.basedir, rep_prefix + '.PRM')
        ref_prm  = os.path.join(self.basedir, ref_prefix + '.PRM')

        # TODO: define 1st image for line, in the example we have no more
        tmp_da = 0

        # generate PRM, LED
        self._make_s1a_tops(burst, date, debug=debug)

        # compute the time difference between first frame and the rest frames
        t1, prf = PRM.from_file(rep_prm).get('clock_start', 'PRF')
        t2      = PRM.from_file(rep_prm).get('clock_start')
        nl = int((t2 - t1)*prf*86400.0+0.2)
        #echo "Shifting the reference PRM by $nl lines..."

        # Shifting the reference PRM by $nl lines...
        # shift the super-references PRM based on $nl so SAT_llt2rat gives precise estimate
        prm1 = PRM.from_file(ref_prm)
        prm1.set(prm1.sel('clock_start' ,'clock_stop', 'SC_clock_start', 'SC_clock_stop') + nl/prf/86400.0)
        tmp_prm = prm1

        # compute whether there are any image offset
        #if tmp_da == 0:
        # tmp_prm defined above from {reference}.PRM
        prm1 = tmp_prm.calc_dop_orb(earth_radius, inplace=True, debug=debug)
        prm2 = PRM.from_file(rep_prm).calc_dop_orb(earth_radius, inplace=True, debug=debug).update()
        lontie,lattie = prm1.SAT_baseline(prm2, debug=debug).get('lon_tie_point', 'lat_tie_point')
        tmp_am = prm1.SAT_llt2rat(coords=[lontie, lattie, 0], precise=1, debug=debug)[1]
        tmp_as = prm2.SAT_llt2rat(coords=[lontie, lattie, 0], precise=1, debug=debug)[1]
        # bursts look equal to rounded result int(np.round(...))
        tmp_da = int(tmp_as - tmp_am)
        #print ('tmp_am', tmp_am, 'tmp_as', tmp_as, 'tmp_da', tmp_da)

        # in case the images are offset by more than a burst, shift the super-reference's PRM again
        # so SAT_llt2rat gives precise estimate
        if abs(tmp_da) >= 1000:
            prf = tmp_prm.get('PRF')
            tmp_prm.set(tmp_prm.sel('clock_start' ,'clock_stop', 'SC_clock_start', 'SC_clock_stop') - tmp_da/prf/86400.0)
            #raise Exception('TODO: Modifying reference PRM by $tmp_da lines...')

        # tmp.PRM defined above from {reference}.PRM
        prm1 = tmp_prm.calc_dop_orb(earth_radius, inplace=True, debug=debug)
        tmpm_dat = prm1.SAT_llt2rat(coords=topo_llt, precise=1, debug=debug)
        prm2 = PRM.from_file(rep_prm).calc_dop_orb(earth_radius, inplace=True, debug=debug)
        tmp1_dat = prm2.SAT_llt2rat(coords=topo_llt, precise=1, debug=debug)

        # get r, dr, a, da, SNR table to be used by fitoffset.csh
        offset_dat0 = np.hstack([tmpm_dat, tmp1_dat])
        func = lambda row: [row[0],row[5]-row[0],row[1],row[6]-row[1],100]
        offset_dat = np.apply_along_axis(func, 1, offset_dat0)

        # define radar coordinates extent
        rmax, amax = PRM.from_file(rep_prm).get('num_rng_bins','num_lines')

        # prepare the offset parameters for the stitched image
        # set the exact borders in radar coordinates
        par_tmp = offset_dat[(offset_dat[:,0]>0) & (offset_dat[:,0]<rmax) & (offset_dat[:,2]>0) & (offset_dat[:,2]<amax)]
        par_tmp[:,2] += nl
        if abs(tmp_da) >= 1000:
            par_tmp[:,2] -= tmp_da
            par_tmp[:,3] += tmp_da

        # prepare the rshift and ashift look up table to be used by make_s1a_tops
        # use tmp_dat instead of offset_dat
        r_xyz = offset_dat[:,[0,2,1]]
        a_xyz = offset_dat[:,[0,2,3]]

        r_grd = self._offset2shift(r_xyz, rmax, amax)
        r_grd_filename = rep_prm[:-4]+'_r.grd'
        r_grd.to_netcdf(r_grd_filename, engine=self.netcdf_engine_write)
        # drop the temporary file at the end of the function
        cleanup.append(r_grd_filename)

        a_grd = self._offset2shift(a_xyz, rmax, amax)
        a_grd_filename = rep_prm[:-4]+'_a.grd'
        a_grd.to_netcdf(a_grd_filename, engine=self.netcdf_engine_write)
        # drop the temporary file at the end of the function
        cleanup.append(a_grd_filename)

        # generate the image with point-by-point shifts
        # note: it removes calc_dop_orb parameters from PRM file
        # generate PRM, LED
        self._make_s1a_tops(burst=burst, date=date, mode=1,
                           rshift_fromfile=f'{rep_prefix}_r.grd',
                           ashift_fromfile=f'{rep_prefix}_a.grd',
                           debug=debug)

        # need to update shift parameter so stitch_tops will know how to stitch
        #PRM.from_file(rep_prm).set(PRM.fitoffset(3, 3, offset_dat)).update()

        # Restoring $tmp_da lines shift to the image... 
        PRM.from_file(rep_prm).set(ashift=0 if abs(tmp_da) < 1000 else tmp_da, rshift=0).update()

        PRM.from_file(rep_prm).set(PRM.fitoffset(3, 3, par_tmp)).update()

        PRM.from_file(rep_prm).calc_dop_orb(earth_radius, 0, inplace=True, debug=debug).update()

        # cleanup
        for filename in cleanup:
            #if os.path.exists(filename):
            os.remove(filename)

    # 'threading' for Docker and 'loky' by default
    def compute_align(self, geometry='auto', bursts=None, dates=None, n_jobs=-1, degrees=12.0/3600, joblib_aligning_backend=None, debug=False):
        """
        Stack and align scenes.

        Parameters
        ----------
        dates : list or None, optional
            List of dates to process. If None, process all scenes. Default is None.
        n_jobs : int, optional
            Number of parallel processing jobs. n_jobs=-1 means all processor cores are used. Default is -1.

        Returns
        -------
        None

        Examples
        --------
        stack.align()
        """
        import numpy as np
        import geopandas as gpd
        from tqdm.auto import tqdm
        import joblib
        import warnings
        # supress warnings about unary_union/union_all() future behaviour to replace None by empty collection
        warnings.filterwarnings('ignore')

        if joblib_aligning_backend is not None:
            print('Note: the joblib_aligning_backend argument has been removed from the compute_align() function.')

        if bursts is None:
            bursts = self.df.index.get_level_values(0).unique()
        if dates is None:
            dates = self.df.index.get_level_values(1).unique()
        dates_rep = [date for date in dates if date != self.reference]

        if n_jobs is None or debug == True:
            print ('Note: sequential joblib processing is applied when "n_jobs" is None or "debug" is True.')
            joblib_backend = 'sequential'
        else:
            joblib_backend = None

        # prepare reference scene
        #self.stack_ref()
        with self.tqdm_joblib(tqdm(desc='Preparing Reference', total=1)) as progress_bar:
            joblib.Parallel(n_jobs=n_jobs, backend=joblib_backend)\
                (joblib.delayed(self._align_ref)(burst, debug=debug) for burst in bursts)

        # prepare secondary images
        with self.tqdm_joblib(tqdm(desc='Aligning Repeat', total=len(dates_rep))) as progress_bar:
            # threading backend is the only one working inside Docker container to run multiple binaries in parallel
            joblib.Parallel(n_jobs=n_jobs, backend=joblib_backend)\
                (joblib.delayed(self._align_rep)(burst, date, degrees=degrees, debug=debug) \
                    for date in dates_rep for burst in bursts)

        