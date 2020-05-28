from __future__ import division
import matplotlib.pyplot as plt
import csv
import pandas as pd
from matplotlib.patches import Patch

user_path = "../../out/dataset_statistics/user.csv"
user_record_distribution_hist = "../../out/distribution_hist.png"

def group_user(file_path):
    with open(file_path) as users:
        reader = csv.reader(users)
        ids = []
        names = []
        descriptions = []
        for row in reader:
            ids.append(row[0])
            names.append(row[1])
            descriptions.append(row[2])
        user_df = pd.DataFrame({'id': ids, 'name': names, 'descriptions': descriptions})
        user_grouped = user_df.groupby('id')
        ids = []
        records_num = []
        for index, data in user_grouped:
            ids.append(index)
            records_num.append(len(data))
        N, bins, patches = plt.hist(records_num, bins=100)
        patches[0].set_facecolor('b')
        for i in range(1, len(patches)):
            patches[i].set_facecolor('r')
        plt.yscale('log')
        plt.xlabel("# of reported tweets")
        plt.ylabel("# of users ($\mathregular{log_{10}}$)")
        legend_elements = [Patch(facecolor='b', edgecolor='b',
                                 label='Occasionally Reported User'),
                           Patch(facecolor='r', edgecolor='r',
                                 label='Frequently Reported User')]
        plt.legend(handles=legend_elements, loc='best')
        plt.savefig(user_record_distribution_hist)
        plt.show()

        count_all = len(records_num)
        count_larger_than_10 = 0
        for i in records_num:
            if i >= 10:
                count_larger_than_10 = count_larger_than_10+1
        result = count_larger_than_10/count_all
        print ("% of user that are reported more than 100 = ")
        print '%.4f%%' % (result*100)

        # # exclude users that has been reported less than 10 times
        # records_num_larger_than_10 = [x for x in records_num if x >= 10]
        # # exclude users that has been reported less than 100 times
        # records_num_larger_than_100 = [x for x in records_num if x >= 100]
        #
        # # Single box plots
        # box(records_num, user_record_0_distribution_path, 'Number of reported tweets per user - Box Plot')
        # box(records_num_larger_than_10, user_record_10_distribution_path,
        #     'Number of reported tweets per user (>=10 posts) - Box Plot')
        # box(records_num_larger_than_100, user_record_100_distribution_path,
        #     'Number of reported tweets per user (>=100 posts) - Box Plot')

        new_user_df = pd.DataFrame({'id': ids, 'num_of_records': records_num})
        new_user_df.sort_values(by='num_of_records', axis=0, ascending=False, inplace=True)
        count_top_10 = 0
        for i in range(10):
            count_top_10 = count_top_10+new_user_df["num_of_records"].iloc[i]
        result = 1-(count_top_10/count_all)
        print ("Top 10 user sends:")
        print '%.4f%%' % (result*100)

        print ("Top 10 reported user: ")
        print new_user_df.iloc[:10]

# Generate box plots for the number of reported tweets per user
group_user(user_path)


# import seaborn as sns
# from collections import Counter
# user_record_0_distribution_path = "../../out/distribution_0.png"
# user_record_10_distribution_path = "../../out/distribution_1.png"
# user_record_100_distribution_path = "../../out/distribution_2.png"

# def make_labels(ax, boxplot):
#     # Grab the relevant Line2D instances from the boxplot dictionary
#     iqr = boxplot['boxes'][0]
#     caps = boxplot['caps']
#     med = boxplot['medians'][0]
#     fly = boxplot['fliers'][0]
#
#     # The x position of the median line
#     xpos = med.get_xdata()
#
#     # Lets make the text have a horizontal offset which is some
#     # fraction of the width of the box
#     xoff = 0.10 * (xpos[1] - xpos[0])
#
#     # The x position of the labels
#     xlabel = xpos[1] + xoff
#
#     # The median is the y-position of the median line
#     median = med.get_ydata()[1]
#
#     # The 25th and 75th percentiles are found from the
#     # top and bottom (max and min) of the box
#     pc25 = iqr.get_ydata().min()
#     pc75 = iqr.get_ydata().max()
#
#     # The caps give the vertical position of the ends of the whiskers
#     capbottom = caps[0].get_ydata()[0]
#     captop = caps[1].get_ydata()[0]
#
#     # Make some labels on the figure using the values derived above
#     ax.text(xlabel, median,
#             'Median = {:6.3g}'.format(median), va='center')
#     ax.text(xlabel, pc25,
#             '25th percentile = {:6.3g}'.format(pc25), va='center')
#     ax.text(xlabel, pc75,
#             '75th percentile = {:6.3g}'.format(pc75), va='center')
#     ax.text(xlabel, capbottom,
#             'Bottom cap = {:6.3g}'.format(capbottom), va='center')
#     ax.text(xlabel, captop,
#             'Top cap = {:6.3g}'.format(captop), va='center')
#
#     # Many fliers, so we loop over them and create a label for each one
#     for flier in fly.get_ydata():
#         ax.text(1 + xoff, flier,
#                 'Flier = {:6.3g}'.format(flier), va='center')
#
#
# def box(data, file_path, title):
#     # Make the figure
#     red_diamond = dict(markerfacecolor='r', marker='D')
#     fig3, ax3 = plt.subplots()
#     ax3.set_title(title)
#
#     # Create the boxplot and store the resulting python dictionary
#     my_boxes = ax3.boxplot(data, flierprops=red_diamond)
#
#     # Call the function to make labels
#     make_labels(ax3, my_boxes)
#     plt.yscale('log')
#     plt.ylabel('number of reported tweets per user')
#     plt.xlabel('dataset of reported tweet ')
#     plt.savefig(file_path)
#     plt.show()



