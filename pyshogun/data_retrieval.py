# encoding: utf-8
# module data_retrieval
# from (pyshogun)
# by __discofocx__

from __future__ import print_function

"""
Data Retrieval functions and other objects.

"""

# imports
from collections import Counter

# functions


def find_full_body_gaps_deprecated(client, character, padding_frames=20):
    """
    Find and return all full body gaps on a character's markers
    :param client: object, valid ViconShogunPost instance, connection to the Vicon Shogun application
    :param character: object, valid ViconShogunPostSDK.Object instance type Character, the character to find gaps on
    :param padding_frames: int, optional, amount of leading and trailing frames to consider in the gap

    :return: list of tuples, [g1(in, out), g2(in, out), g3(in, out) ... gn(in, out)] where g is a gap
    """
    found_gaps = list()
    character_has_gaps = True

    # Go to the play start
    client.Timeline.SetTimeFrames(client.Timeline.GetPlayStart())

    # Select character markers
    client.HSL('select {char};SelectByType_Marker_ThisCharacter;'.format(char=character.Name))

    # Find gaps like they're hot
    while character_has_gaps:
        gap = client.HSL('findGap -noLoop;')
        if gap != '':
            gap_in, gap_out = gap.split(',')
            found_gaps.append((int(gap_in) - padding_frames, int(gap_out) + padding_frames))
            client.Timeline.SetTimeFrames(int(gap_out) + padding_frames)
        else:
            character_has_gaps = False

    return found_gaps


def find_full_body_gaps(client, character, padding_frames=20):
    """
    Find and return all full body gaps on a character's markers
    :param client: object, valid ViconShogunPost instance, connection to the Vicon Shogun application
    :param character: object, valid ViconShogunPostSDK.Object instance type Character, the character to find gaps on
    :param padding_frames: int, optional, amount of leading and trailing frames to consider in the gap
    :return: list of tuples, [g1(in, out), g2(in, out), g3(in, out) ... gn(in, out)] where g is a gap
    """

    # Get character markers
    markers = [m for m in character.GetChildren() if m.Type == 'Marker']

    # Find gaps in markers
    marker_gaps = dict()
    for marker in markers:
        marker_gap = client.HSL('getGaps({marker});'.format(marker=marker.Path))
        if marker_gap != '':
            marker_gaps[marker.Path] = marker_gap
        else:
            pass

    # Compare the gaps and find the most common occurrences
    try:
        compare_gaps = Counter(marker_gaps.values())
        most_common_gaps = compare_gaps.most_common()[0][0]
    except IndexError:  # In case we did not find any gaps
        return None
    else:
        # Format the data string coming from the client
        full_body_gaps = [int(gap) for gap in most_common_gaps.split(',')]
        found_gaps = zip(full_body_gaps[:-1:2], full_body_gaps[1::2])
        # Add the frame padding
        padded_gaps = [(gin - padding_frames, gout + padding_frames) for (gin, gout) in found_gaps]

        return padded_gaps
