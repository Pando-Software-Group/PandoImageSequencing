"""
====================================
Filename:         orientation.py 
Author:              Joseph Farah 
Description:       Contains classes and methods for orientation of 
                    img files.
====================================
Notes
     
"""
#------------- imports -------------#
import os
import copy
import numpy as np
import datetime as dt
from tqdm import tqdm



#------------- classes -------------#
class Point(object):

    def __init__(self, timestamp, fpath, slate, im, dng):

        self.timestamp = timestamp
        self.fpath = fpath
        self.dng = dng
        self.slate = slate
        self.im = im
        self.tag = self.fpath.split('/')[-1].split('.')[0]
        self.timestamp_old = timestamp

    def __sub__(self, other):
        diff = self.timestamp - other.timestamp
        return diff.seconds

    @staticmethod
    def get_tag(path):
        return path.split('/')[-1].split('.')[0]


#------------- functions -------------#
def statistical_sequence(points, start_index, end_index, output_path):
    points_replace = []

    first_half_bin = []
    second_half_bin = []

    first_half_bin.append(points[start_index])


    for p, point in enumerate(points):

        if point.timestamp < points[start_index].timestamp:
            second_half_bin.append(point)
        elif point.timestamp > points[end_index].timestamp:
            first_half_bin.append(point)

        elif point.timestamp == points[start_index].timestamp or point.timestamp == points[end_index].timestamp:
            continue

        else:
            points_replace.append(point)




    #------------- build model for each -------------#
    diffs_first_half_mean = np.mean(np.diff(first_half_bin[1:]))
    diffs_first_half_std = np.std(np.diff(first_half_bin[1:]))

    diffs_second_half_mean = np.mean(np.diff(second_half_bin))
    diffs_second_half_std = np.std(np.diff(second_half_bin))

    diffs_combined_mean = np.mean(np.concatenate([np.diff(second_half_bin), np.diff(first_half_bin[1:])]))
    diffs_combined_std = np.std(np.concatenate([np.diff(second_half_bin), np.diff(first_half_bin[1:])]))


    #------------- perform probability sort -------------#

    ## set marker ##
    fh_marker = 1
    sh_marker = -1

    ## begin by iterating through every point chrono ##
    SKIP = False
    for p, point in enumerate(points_replace):

        if SKIP: 
            SKIP = False
            continue

        ## point must either belong immediately 
        ## after last point in first_half_bin 
        ## or immediately after last point in
        ## second half bin, excluding start/end

        # probability of lying after LP in FHB 
        sigma_prob_FH = (point - first_half_bin[fh_marker-1]-diffs_first_half_mean)/diffs_first_half_std

        # probability of lying after LP in SHB
        sigma_prob_SH = (point - second_half_bin[sh_marker]-diffs_second_half_mean)/diffs_second_half_std

        print(point - first_half_bin[fh_marker-1], point - second_half_bin[sh_marker], sigma_prob_FH, sigma_prob_SH)

        # lower sigma indicates higher probability 
        if sigma_prob_FH < sigma_prob_SH:
            first_half_bin.insert(fh_marker, point)
            if p < len(points_replace)-1:
                second_half_bin.insert(sh_marker, points_replace[p+1])
        else:
            if p < len(points_replace)-1:
                second_half_bin.append(points_replace[p+1])
            first_half_bin.insert(fh_marker, point)

        SKIP = True
        fh_marker+=1

    second_half_bin.append(points[end_index])

    second_half_bin = sorted(second_half_bin, key=lambda x:x.timestamp)
    first_half_bin = sorted(first_half_bin, key=lambda x:x.timestamp)

    # for p, point in enumerate(first_half_bin):
    #     plt.scatter(p, point.timestamp)

    # plt.title("First half bin")
    # plt.show()


    # for p, point in enumerate(second_half_bin):
    #     plt.scatter(p, point.timestamp)

    # plt.title("Second half bin")
    # plt.show()




    #------------- merge lists -------------#
    def time_plus(time, timedelta):
        start = dt.datetime(
            2000, 1, 1,
            hour=time.hour, minute=time.minute, second=time.second)
        end = start + timedelta
        end = dt.datetime(
            2000, 1, 1,
            hour=end.hour, minute=end.minute, second=end.second)
        return end

    start_time = dt.time(6,1,0)
    end_time = dt.time(7,6,0)

    bad_start_time = points[start_index].timestamp

    new_points = []
    for point in first_half_bin:
        pointcopy = copy.deepcopy(point)

        time_elapsed_bad_start = pointcopy.timestamp - bad_start_time
        pointcopy.timestamp = time_plus(start_time, time_elapsed_bad_start)
        new_points.append(pointcopy)


    bad_start_time = second_half_bin[0].timestamp
    sh_start_time = time_plus(new_points[-1].timestamp, dt.timedelta(seconds=6*diffs_combined_mean))


    for point in second_half_bin:
        pointcopy = copy.deepcopy(point)

        time_elapsed_bad_start = pointcopy.timestamp - bad_start_time
        pointcopy.timestamp = time_plus(sh_start_time, time_elapsed_bad_start)
        new_points.append(pointcopy)





    for p, point in enumerate(tqdm(new_points)):
        os.system(f"cp '{point.fpath}' {output_path}/jpgs/{p}_{point.tag}_{p}_new-time={str(point.timestamp).replace(' ', '_')}.jpg")
        os.system(f"cp '{point.dng}' {output_path}/dngs/{p}_{point.tag}_{p}_new-time={str(point.timestamp).replace(' ', '_')}.dng")
        # if point.slate in ['open', 'end']:
        #     plt.scatter(p, point.timestamp, marker='*')
        # else:
        #     plt.scatter(p, point.timestamp)

    # plt.title("Merged")
    # plt.show()

    print(f"END SLATE: {end_time}. Predicted from merge: {new_points[-1].timestamp}")


    return first_half_bin, second_half_bin, new_points, diffs_combined_mean




def suggest_reordering(points, first_half_bin, second_half_bin, output_path, start_index, end_index, diffs_combined_mean):

    print("Which images are bad?")
    bad_images = []
    while 1:
        num = input("Enter number, any other char will break >>> ")
        try: 
            num = int(num)
        except ValueError:
            break
        bad_images.append(num)


    fh_badims, sh_badims = [], []
    for idx in bad_images:
        if idx > len(first_half_bin):
            sh_badims.append(idx-len(first_half_bin))
        else:
            fh_badims.append(idx)


    new_second_half_bin = copy.deepcopy(second_half_bin)
    new_first_half_bin = copy.deepcopy(first_half_bin)

    for idx in sh_badims:
        new_first_half_bin.append(new_second_half_bin[idx])
    for idx in fh_badims:
        new_second_half_bin.append(new_first_half_bin[idx])


    for i in sorted(fh_badims, reverse=True):
        del new_first_half_bin[i]

    for i in sorted(sh_badims, reverse=True):
        del new_second_half_bin[i]

         


    new_second_half_bin = sorted(new_second_half_bin, key=lambda x:x.timestamp)
    new_first_half_bin = sorted(new_first_half_bin, key=lambda x:x.timestamp)

    # for p, point in enumerate(new_first_half_bin):
    #     plt.scatter(p, point.timestamp)

    # plt.title("First half bin")
    # plt.show()


    # for p, point in enumerate(new_second_half_bin):
    #     plt.scatter(p, point.timestamp)

    # plt.title("Second half bin")
    # plt.show()




    #------------- merge lists -------------#
    def time_plus(time, timedelta):
        start = dt.datetime(
            2000, 1, 1,
            hour=time.hour, minute=time.minute, second=time.second)
        end = start + timedelta
        end = dt.datetime(
            2000, 1, 1,
            hour=end.hour, minute=end.minute, second=end.second)
        return end

    start_time = dt.time(6,1,0)
    end_time = dt.time(7,6,0)

    bad_start_time = points[start_index].timestamp

    new_points = []
    for point in new_first_half_bin:
        pointcopy = copy.deepcopy(point)

        time_elapsed_bad_start = pointcopy.timestamp - bad_start_time
        pointcopy.timestamp = time_plus(start_time, time_elapsed_bad_start)
        new_points.append(pointcopy)


    bad_start_time = new_second_half_bin[0].timestamp
    sh_start_time = time_plus(new_points[-1].timestamp, dt.timedelta(seconds=6*diffs_combined_mean))


    for point in new_second_half_bin:
        pointcopy = copy.deepcopy(point)

        time_elapsed_bad_start = pointcopy.timestamp - bad_start_time
        pointcopy.timestamp = time_plus(sh_start_time, time_elapsed_bad_start)
        new_points.append(pointcopy)




    os.system(f"rm -rf {output_path}")
    os.system(f"mkdir {output_path}")
    os.system(f"mkdir {output_path}/jpgs/")
    os.system(f"mkdir {output_path}/dngs/")

    for p, point in enumerate(tqdm(new_points)):
        os.system(f"cp '{point.fpath}' {output_path}/jpgs/{p}_{point.tag}_{p}_new-time={str(point.timestamp).replace(' ', '_')}.jpg")
        os.system(f"cp '{point.dng}' {output_path}/dngs/{p}_{point.tag}_{p}_new-time={str(point.timestamp).replace(' ', '_')}.dng")
        # if point.slate in ['open', 'end']:
        #     plt.scatter(p, point.timestamp, marker='*')
        # else:
        #     plt.scatter(p, point.timestamp)

    # plt.title("Merged")
    # plt.show()

    print(f"END SLATE: {end_time}. Predicted from merge: {new_points[-1].timestamp}")


    return new_first_half_bin, new_second_half_bin, new_points, bad_images


