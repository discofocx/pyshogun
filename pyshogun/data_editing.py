# encoding: utf-8
# module data_editing
# from (pyshogun)
# by __discofocx__

from __future__ import print_function

"""
Data Editing functions and other objects.

"""

# imports

# functions


def freeze_marker_range(client, markers, range_in, range_out):
    """
    Freeze the marker(s) translation for a certain amount of time (range),
    Useful for situations where the character leaves the capture volume or big unhandled gaps

    :param client: object, valid ViconShogunPost instance, connection to the Vicon Shogun application
    :param markers: list of objects, valid ViconShogunPostSDK.Object type Marker, marker(s) to freeze
    :param range_in: int, Start frame for the freeze range, this is the frame that will get frozen
    :param range_out: int, End frame for the freeze range
    :return: None
    """

    # client.Timeline.SetTimeFrames(range_in)
    exclude = ['LTHM3', 'LIDX3', 'LPNK3',
               'RTHM3', 'RIDX3', 'RPNK3']

    # Select markers
    for marker in markers:
        if marker.Type != 'Marker':
            pass
        else:
            if marker.Name in exclude:
                print(marker.Name)
                pass
            else:
                client.HSL('select -a {marker};'.format(marker=marker.Path))
                # Copy the values from the range in to the range out
                marker.Translation.X[range_out] = marker.Translation.X[range_in]
                marker.Translation.Y[range_out] = marker.Translation.Y[range_in]
                marker.Translation.Z[range_out] = marker.Translation.Z[range_in]

    # Set linear interpolation on all selected markers
    client.HSL('setInterpType Translation Linear;')
    # Cut any keys that exist in-between the freeze range
    client.HSL('selectRange {rin} {rout};cutKeys -ranges;'.format(rin=(range_in + 1), rout=(range_out - 1)))
    # Interpolate the gap
    client.HSL('fillGaps -ranges;')
    # Clean Selection
    client.HSL('select;selectRange;')
