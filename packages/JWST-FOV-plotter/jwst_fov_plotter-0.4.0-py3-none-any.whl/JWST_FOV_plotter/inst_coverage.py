import numpy as np
import pandas as pd
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from JWST_FOV_plotter.auxiliar_functions import aper_translator


def point_in_polygon(x, y, verts):
    """
    Tells whether a point falls within an N-side polygon delimited by N given
    vertices coordinates.

    Arguments:
    x -- x coordinate of the point.
    y -- y coordinate of the point.
    verts -- Nx2 matrix with the coordinates of the N vertices of the polygon.

    Returns:
    is_inside -- boolean. True if the point is enclosed within the polygon.
    """

    point = Point(x, y)

    poly = []
    for i in range(len(verts)):
        poly.append([verts[i, 0], verts[i, 1]])

    polygon = Polygon(poly)

    is_inside = polygon.contains(point)

    return is_inside


def inst_cov(coords, fovs):
    """
    Tells the instrument coverage obtained at any particular coordinates with
    some JWST pointings.

    Arguments:
    coords -- Nx2 matrix with the coordinates of the N points on the sky to
              check.
    fovs --


    Returns:
    inst_cov -- N-dimensional vector including the instruments coverage of each
                sky coordinates.
    """

    # Adjusting the cases for a single input point to check (not a matrix)
    # and/or single input pointing FOV (single DataFrame, not list of
    # DataFrames).
    if len(np.shape(coords)) == 1:
        coords = [coords]
    if type(fovs) not in [np.array, list]:
        fovs = [fovs]

    # Defining DataFrame to fill with the coverage of each input point.
    inst_cov = pd.DataFrame(np.array(coords), columns=['ra', 'dec'])
    inst_cov['instr_cover'] = ''

    # Checking the coverage of each point.
    for ra, dec in coords:
        cover_p = []
        # Checking the coverage of this point in every pointing.
        for fov in fovs:
            # Checking the coverage of the point in every aperture of the
            # pointing.
            for inst, aper in zip(fov.Instrument, fov.Aperture):
                row = fov.loc[fov.Aperture == aper].iloc[0]
                # Vertices of this particular aperture.
                vert = np.array([[row.RA_1, row.DEC_1], [row.RA_2, row.DEC_2],
                                 [row.RA_3, row.DEC_3], [row.RA_4, row.DEC_4]])

                if point_in_polygon(ra, dec, vert):
                    aper_str = aper_translator(aper)
                    # Skipping apertures already written to avoid redundancy.
                    if aper_str not in cover_p:
                        cover_p.append(aper_str)

        # Adding a str with the instrument coverage for this point.
        cover_p_str = ''
        for cps in cover_p:
            cover_p_str += ' %s' % cps
        cond = (inst_cov.ra == ra) & (inst_cov.dec == dec)
        inst_cov.loc[cond, 'instr_cover'] = cover_p_str

    return inst_cov
