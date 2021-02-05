# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 18:35:31 2021

@author: Sam


'Fantasy' Six Nations analysis for twitter

"""


""" Import required modules """
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns
import themepy
import requests
from PIL import Image
from io import BytesIO




""" Load and format data """
## Load in data
data = pd.DataFrame(pd.read_excel('C:/Users/Sam/Documents/Sports Data Science and Analysis/Rugby/Six Nations 2021/Fantasy Analysis.xlsx', sheet_name='2020 Stats Breakdown', engine='openpyxl'))
# data.head(10)


## Remove spaces that were at end of each column name
data.columns = data.columns.str.strip()


## Calculate variables of interest
data['Carries per min']   = data['CA']/data['MP']
data['Carries per match'] = data['Carries per min']*80
data['Metres per carry']  = data['M']/data['CA']

data['T per min']         = data['TM']/data['MP']
data['T per match']       = data['T per min']*80
data['DT per min']        = data['DT']/data['MP']
data['DT per match']      = data['DT per min']*80
data['T:DT']              = data['T per match']/data['DT per match']


## Create new dataframe with players who played 80 mins or more total
data80 = data[data['MP'] > 79]


medianCarPerMat = round(data80['Carries per match'].median(), 1)
medianMetPerCar = round(data80['Metres per carry'].median(), 1)
meanCarPerMat = round(data80['Carries per match'].mean(), 1)
meanMetPerCar = round(data80['Metres per carry'].mean(), 1)


scatterPlayers = data80[data80['Carries per match'] > 13]
scatterPlayers = scatterPlayers.append(data80[data80['Metres per carry'] > 10])
# scatterPlayers = scatterPlayers.reset_index(drop=True)

swarmPlayers = data[data['M'] > 310].reset_index(drop=True)

tDTPlayers = data80[data80['T:DT'] < 4.49]
tDTPlayers = tDTPlayers.append(data80[data80['T per match'] > 20])
# tDTPlayers = tDTPlayers.reset_index(drop=True)

""" Setup theme for plots """
theme = themepy.Theme()

theme.set_theme() # ensures set to default matplotlib rcParams

(theme
 .set_font("Alegreya Sans", color="w") # sets default font and text color
 .set_pips(False) # turns off tick lines
 .set_spines("off", which=["top","right"], color="w") # turns off top and right ax borders & sets color of others to white
 .set_background("#313332") # sets the fig, axis, and savefig facecolors
 .set_ticklabel_size(12) # sets size of tick labels
 .set_plot_colors("grey", "red")  # sets first three colors of cycler and also colors of theme.primary_color, theme.secondary_color, and theme.tertiary_color
)




""" 1. Swarmplot of metres made """
# Swarmplot of metres made for all players

# Plot the data
fig, ax = plt.subplots(figsize=(7,5))
sns.swarmplot(x=data['M'], color=theme.primary_color)

# Remove spines for swarmplot
sns.despine(left=True, bottom=True)

# Add grid lines and format
ax.grid(axis='x', linewidth=.5, linestyle=':', zorder=1, color='lightgrey')

# Add title and subtitle
plt.suptitle("Metres Made",
              **theme.title_font, fontsize=16, fontweight="bold", x=0.136, y=0.95)
plt.title("Metres made by all players across the Six Nations 2020 tournament.",
          **theme.title_font, fontsize=10, loc='left')

# Add names and colour for standout players
sns.swarmplot(x=swarmPlayers['M'], color=theme.secondary_color)

for x, name in zip(swarmPlayers['M'], swarmPlayers['PLAYER'].str.strip()):
    if name != 'Jayden Hayward' and name != 'Nick Tompkins':
        plt.text(x-5,-0.03, name, fontsize=8, rotation=270)
    elif name == 'Nick Tompkins':
        plt.text(x-5,0.23, name, fontsize=8, rotation=270)
    elif name == 'Jayden Hayward':
        plt.text(x-5,-0.05, name, fontsize=8, rotation=270)
        
# Add axis labels
ax.set_xlabel('Total Metres Made (m)')

# Add logo
ax2 = fig.add_axes([0.85,0.85,0.125,0.125])
ax2.axis('off')
url = "https://d2cx26qpfwuhvu.cloudfront.net/sixnations/wp-content/uploads/2019/02/09121742/GUINNESS_SIX_NATIONS_LANDSCAPE_STACKED_RGB.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
ax2.imshow(img)

# Add Credits
fig.text(0.01,0.01, "Created by Sam Jones / @SJBiomech. \nData from: sixnationsrugby.com/statistics",
          fontstyle='italic', fontsize=8, fontfamily='Alegreya Sans')

plt.tight_layout()
plt.show()

# plt.savefig('metresSwarmplot', bbox_inches='tight', dpi=300)




""" 2. Scatter of carries per 80 against avg metres per carry """
# This for players who played minimum of 80 mins

# Create figure and axes
fig, ax = plt.subplots(figsize=(7,5))

# Plot scatter points
ax.scatter(data80['Carries per match'], data80['Metres per carry'],
           color=theme.primary_color, # the first colour in cycle, our primary color
           edgecolors=theme.background, # our background colour (figure.facecolor)
           s=50,
           zorder=5,
           alpha=0.75)

# Remove spines
sns.despine(right=True, top=True)

# Add major gridlines
plt.grid(axis='both', linestyle='-', alpha=0.25, color='lightgrey', lw=0.5)

# Add mean lines and mean text
ax.plot([meanCarPerMat,meanCarPerMat],[-10,30],'k-', linestyle = "--", lw=0.75, color='w')
ax.plot([-10,30],[meanMetPerCar,meanMetPerCar],'k-', linestyle = "--", lw=0.75, color='w')

plt.text(20.1, meanMetPerCar-0.75, '{} m'.format(meanMetPerCar))
plt.text(meanCarPerMat+0.1, 13.75, '{} carries'.format(meanCarPerMat), rotation=270)

# Add standout players
for x,y,name in zip(scatterPlayers['Carries per match'],scatterPlayers['Metres per carry'], scatterPlayers['PLAYER'].str.strip()):
    
    # Name bottom and left of marker
    if name == 'Anthony Watson' or name == 'Stuart Hogg' or name =='Sebastian Negri':
        ax.scatter(x,y,
                   color=theme.secondary_color,
                   edgecolors=theme.background,
                   s=50,
                   alpha=1,
                   zorder=6)
        t = ax.text(x, y-0.55, name, fontsize=6, zorder=7, ha='right')
        
    # Name bottom and right of marker
    elif name == 'Hadleigh Parkes':
        ax.scatter(x,y,
                   color=theme.secondary_color,
                   edgecolors=theme.background,
                   s=50,
                   alpha=1,
                   zorder=6)
        t = ax.text(x, y-0.7, name, fontsize=6, zorder=7)
        
    # Name top and left of marker
    elif name == 'Gregory Alldritt':
        ax.scatter(x,y,
                    color=theme.secondary_color,
                    edgecolors=theme.background,
                    s=50,
                    alpha=1,
                    zorder=6)
        t = ax.text(x, y+0.25, name, fontsize=6, zorder=7, ha='right')
        
    # Name top and right of marker
    else:
        ax.scatter(x,y,
                   color=theme.secondary_color,
                   edgecolors=theme.background,
                   s=50,
                   alpha=1,
                   zorder=6)
        t = ax.text(x, y+0.25, name, fontsize=6, zorder=7)
        
    t.set_path_effects([path_effects.withStroke(linewidth=3,foreground=theme.background)])    


# Add title and subtitle
fig.suptitle("Carry Rate and Carry Efficiency",
              **theme.title_font, fontsize=16, fontweight="bold", x=0.395, y=0.95)
plt.title("Average metres per carry and carries per 80 minutes."
          "\n"
          "Players included here played a minimum of 80 minutes across the"
          "\nSix Nations 2020 tournament.",
          **theme.title_font, fontsize=10, loc='left')

# Add Credits
fig.text(0.01,0.01, "Created by Sam Jones / @SJBiomech. \nData from: sixnationsrugby.com/statistics",
          fontstyle='italic', fontsize=8, fontfamily='Alegreya Sans')

# Add axis titles
plt.xlabel("Carries per 80 minutes")
plt.ylabel("Average Metres per Carry (m)")

# Add logo
ax2 = fig.add_axes([0.85,0.85,0.125,0.125])
ax2.axis('off')
url = "https://d2cx26qpfwuhvu.cloudfront.net/sixnations/wp-content/uploads/2019/02/09121742/GUINNESS_SIX_NATIONS_LANDSCAPE_STACKED_RGB.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
ax2.imshow(img)

# Set axis limits
ax.set_xlim(-0.5,22.5)
ax.set_ylim(-0.5,18)

plt.tight_layout()
plt.show()

# plt.savefig('metresAndCarriesScatter', bbox_inches='tight', dpi=300)




""" 3. Scatter of dominant tackles per 80 against tackles per 80 """
# This for players who played minimum of 80 mins

# Create figure and axes
fig, ax = plt.subplots(figsize=(7,5))

# Plot scatter points
ax.scatter(data80['T per match'], data80['DT per match'],
           color=theme.primary_color, # the first colour in cycle, our primary color
           edgecolors=theme.background, # our background colour (figure.facecolor)
           s=50,
           zorder=5,
           alpha=0.75)

# Remove spines
sns.despine(right=True, top=True)

# Add major gridlines
plt.grid(axis='both', linestyle='-', alpha=0.25, color='lightgrey', lw=0.5)

# DT to T ratio dividing lines and text in each division
ax.plot([0, 24], [0, 6], # approx 1 in every 4
        ls="--", lw=0.75,
        color="w",
        zorder=2)

ax.plot([0, 36], [0, 6], # approx 1 in every 6
        ls="--", lw=0.75,
        color="w",
        zorder=2)

ax.plot([0, 60], [0, 6], # approx 1 in every 10
        ls="--", lw=0.75,
        color="w",
        zorder=2)

ax.plot([0, 108], [0, 6], # approx 1 in every 18
        ls="--", lw=0.75,
        color="w",
        zorder=2)

# Text for tackle ratio divisions
t1 = ax.text(10.3,4.9, "Players here make\n1 DT on average for\nevery 4 T...",
             alpha=0.75)

t2 = ax.text(20.8,4.5, "...1 DT \nevery 6 T...",
             alpha=0.75)

t3 = ax.text(25.75,3.5, "...1 DT \nevery 10 T...",
             alpha=0.75)

t4 = ax.text(27.1,2.1, "...1 DT \nevery 18 T",
             alpha=0.75)

for t in (t1, t2, t3, t4):
    t.set_path_effects([path_effects.withStroke(linewidth=5,foreground=theme.background)])    

# Add standout players
for x,y,name in zip(tDTPlayers['T per match'],tDTPlayers['DT per match'], tDTPlayers['PLAYER'].str.strip()):
    
    # Name top and left of marker
    if name == 'Joe Marler' or name == 'Romain Taofifenua':
        ax.scatter(x,y,
                   color=theme.secondary_color,
                   edgecolors=theme.background,
                   s=50,
                   alpha=1,
                   zorder=6)
        t = ax.text(x, y+0.1, name, fontsize=6, zorder=7, ha='right')
    
    # Name bottom and right of marker
    elif name == 'Sam Underhill':
        ax.scatter(x,y,
                   color=theme.secondary_color,
                   edgecolors=theme.background,
                   s=50,
                   alpha=1,
                   zorder=6)
        t = ax.text(x+0.1, y-0.25, name, fontsize=6, zorder=7)
        
    # Name top and centre of marker
    elif name == 'Giovanni Licata':
        ax.scatter(x,y,
                   color=theme.secondary_color,
                   edgecolors=theme.background,
                   s=50,
                   alpha=1,
                   zorder=6)
        t = ax.text(x, y+0.1, name, fontsize=6, zorder=7, ha='center')
        
    # Name top and right of marker
    else:
        ax.scatter(x,y,
                   color=theme.secondary_color,
                   edgecolors=theme.background,
                   s=50,
                   alpha=1,
                   zorder=6)
        t = ax.text(x, y+0.1, name, fontsize=6, zorder=7)
        
    t.set_path_effects([path_effects.withStroke(linewidth=3,foreground=theme.background)])    

# Add title and subtitle
fig.suptitle("Tackle Hard and Fast",
              **theme.title_font, fontsize=16, fontweight="bold", x=0.262, y=0.95)
plt.title("Dominant tackles (DT) and tackles (T) per 80 minutes."
          "\n"
          "Players included here played a minimum of 80 minutes across the"
          "\nSix Nations 2020 tournament.",
          **theme.title_font, fontsize=10, loc='left')

# Add Credits
fig.text(0.01,0.01, "Created by Sam Jones / @SJBiomech. \nData from: sixnationsrugby.com/statistics",
          fontstyle='italic', fontsize=8, fontfamily='Alegreya Sans')

# Add axis titles
plt.xlabel("Tackles per 80 minutes")
plt.ylabel("Dominant tackles per 80 minutes")

# Add logo
ax2 = fig.add_axes([0.85,0.85,0.125,0.125])
ax2.axis('off')
url = "https://d2cx26qpfwuhvu.cloudfront.net/sixnations/wp-content/uploads/2019/02/09121742/GUINNESS_SIX_NATIONS_LANDSCAPE_STACKED_RGB.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
ax2.imshow(img)

# Set axis limits
ax.set_xlim(-1,32.9)
ax.set_ylim(-0.25,5.9)

plt.tight_layout()
plt.show()

# plt.savefig('dominantTackleScatter', bbox_inches='tight', dpi=300)


