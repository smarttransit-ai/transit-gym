import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import glob
import os

###table of kj/km for base scenario
path = r'/Traj6-7/RR1'                    
all_files = glob.glob(os.path.join(path, "diesel*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyr1d = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRate']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyr1d.loc[0,c]=energy
    c=c+1
energyr1d.columns=b
#energyr1d = energyr1d.replace([np.inf], np.nan)
#energyr1d.mean()

all_files = glob.glob(os.path.join(path, "hybrid*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyr1h = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRateH']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyr1h.loc[0,c]=energy
    c=c+1
energyr1h.columns=b

all_files = glob.glob(os.path.join(path, "elect*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyr1e = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=df['speed']*(0.01*3.6)*0.621371/3600 #mi/s
    df['energyrate']=(df['Power']*0.02457002457002457*0.28/1000)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyr1e.loc[0,c]=energy
    c=c+1
energyr1e.columns=b

path = r'/Traj6-7/RR3'                    
all_files = glob.glob(os.path.join(path, "diesel*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR3d = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRate']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR3d.loc[0,c]=energy
    c=c+1
energyR3d.columns=b
#energyR3d = energyR3d.replace([np.inf], np.nan)
#energyR3d.mean()

all_files = glob.glob(os.path.join(path, "hybrid*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR3h = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRateH']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR3h.loc[0,c]=energy
    c=c+1
energyR3h.columns=b

all_files = glob.glob(os.path.join(path, "elect*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR3e = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=df['speed']*(0.01*3.6)*0.621371/3600 #mi/s
    df['energyrate']=(df['Power']*0.02457002457002457*0.28/1000)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR3e.loc[0,c]=energy
    c=c+1
energyR3e.columns=b

path = r'/Traj6-7/RR4'                    
all_files = glob.glob(os.path.join(path, "diesel*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR4d = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRate']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR4d.loc[0,c]=energy
    c=c+1
energyR4d.columns=b
#energyR4d = energyR4d.replace([np.inf], np.nan)
#energyR4d.mean()

all_files = glob.glob(os.path.join(path, "hybrid*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR4h = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRateH']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR4h.loc[0,c]=energy
    c=c+1
energyR4h.columns=b

all_files = glob.glob(os.path.join(path, "elect*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR4e = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=df['speed']*(0.01*3.6)*0.621371/3600 #mi/s
    df['energyrate']=(df['Power']*0.02457002457002457*0.28/1000)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR4e.loc[0,c]=energy
    c=c+1
energyR4e.columns=b

path = r'/Traj6-7/RR9'                    
all_files = glob.glob(os.path.join(path, "diesel*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR9d = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRate']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR9d.loc[0,c]=energy
    c=c+1
energyR9d.columns=b
#energyR9d = energyR9d.replace([np.inf], np.nan)
#energyR9d.mean()

all_files = glob.glob(os.path.join(path, "hybrid*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR9h = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRateH']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR9h.loc[0,c]=energy
    c=c+1
energyR9h.columns=b

all_files = glob.glob(os.path.join(path, "elect*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR9e = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=df['speed']*(0.01*3.6)*0.621371/3600 #mi/s
    df['energyrate']=(df['Power']*0.02457002457002457*0.28/1000)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR9e.loc[0,c]=energy
    c=c+1
energyR9e.columns=b

path = r'/Traj6-7/RR10A'                    
all_files = glob.glob(os.path.join(path, "diesel*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR10Ad = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRate']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR10Ad.loc[0,c]=energy
    c=c+1
energyR10Ad.columns=b
#energyR10Ad = energyR10Ad.replace([np.inf], np.nan)
#energyR10Ad.mean()

all_files = glob.glob(os.path.join(path, "hybrid*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR10Ah = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRateH']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR10Ah.loc[0,c]=energy
    c=c+1
energyR10Ah.columns=b

all_files = glob.glob(os.path.join(path, "elect*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR10Ae = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=df['speed']*(0.01*3.6)*0.621371/3600 #mi/s
    df['energyrate']=(df['Power']*0.02457002457002457*0.28/1000)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR10Ae.loc[0,c]=energy
    c=c+1
energyR10Ae.columns=b


path = r'/Traj6-7/RR10G'                    
all_files = glob.glob(os.path.join(path, "diesel*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR10Gd = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRate']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR10Gd.loc[0,c]=energy
    c=c+1
energyR10Gd.columns=b
#energyR10Gd = energyR10Gd.replace([np.inf], np.nan)
#energyR10Gd.mean()

all_files = glob.glob(os.path.join(path, "hybrid*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR10Gh = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRateH']*0.264172/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR10Gh.loc[0,c]=energy
    c=c+1
energyR10Gh.columns=b

all_files = glob.glob(os.path.join(path, "elect*.csv")) 
b=[mine[-33:-4] for mine in all_files]
energyR10Ge = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=df['speed']*(0.01*3.6)*0.621371/3600 #mi/s
    df['energyrate']=(df['Power']*0.02457002457002457*0.28/1000)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyR10Ge.loc[0,c]=energy
    c=c+1
energyR10Ge.columns=b


# =============================================================================
# =============================================================================
###table of kj/km for reduced scenario
path = r'/reduced80traj6-7/Diesel'                    
all_files = glob.glob(os.path.join(path, "diesel*.csv")) 
b=[mine[-27:-4] for mine in all_files]
energyr1d = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRate']/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyr1d.loc[0,c]=energy
    c=c+1
energyr1d.columns=b

path = r'/reduced80traj6-7/Hybrid'                    
all_files = glob.glob(os.path.join(path, "hybrid*.csv")) 
b=[mine[-27:-4] for mine in all_files]
energyr1h = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=0.621371*df['speed']/3600 #mi/s
    df['energyrate']=(df['FuelRateH']/3600)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyr1h.loc[0,c]=energy
    c=c+1
energyr1h.columns=b

path = r'/reduced80traj6-7/Electric'                    
all_files = glob.glob(os.path.join(path, "elect*.csv")) 
b=[mine[-27:-4] for mine in all_files]
energyr1e = pd.DataFrame()
energy=np.float32(0)
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2,10]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(float)
    df['speed']=df['speed']*(0.01*3.6)*0.621371/3600 #mi/s
    df['energyrate']=(df['Power']*0.02457002457002457*0.28/1000)  #gal/s
    energy=df['speed'].sum()/df['energyrate'].sum() #mi/gal
    energyr1e.loc[0,c]=energy
    c=c+1
energyr1e.columns=b
energyall=pd.concat([energyr1d,energyr1h,energyr1e])

































#figure5 left
path = r'E:/SUMO/RUIXIAO/newChattanooganet/Data/output/Traj08'                    
all_files = glob.glob(os.path.join(path, "Route*.csv"))    
df_from_each_file = (pd.read_csv(f, usecols=[2,3]) for f in all_files)
traj08 = pd.concat(df_from_each_file, ignore_index=True)
traj08['speed']=traj08['speed']*(0.01*3.6*0.62137) #mph
traj08['acceleration']=traj08['acceleration']*(0.001) 
traj08 = traj08[(traj08.speed > 5)]

path = r'E:/SUMO/RUIXIAO/newChattanooganet/Data/output/Traj12'                    
all_files = glob.glob(os.path.join(path, "Route*.csv"))    
df_from_each_file = (pd.read_csv(f, usecols=[2,3]) for f in all_files)
traj12 = pd.concat(df_from_each_file, ignore_index=True)
traj12['speed']=traj12['speed']*(0.01*3.6*0.62137) #mph
traj12['acceleration']=traj12['acceleration']*(0.001) 
traj12 = traj12[(traj12.speed > 5)]

path = r'E:/SUMO/RUIXIAO/newChattanooganet/Data/output/Traj17'                    
all_files = glob.glob(os.path.join(path, "Route*.csv"))    
df_from_each_file = (pd.read_csv(f, usecols=[2,3]) for f in all_files)
traj17 = pd.concat(df_from_each_file, ignore_index=True)
traj17['speed']=traj17['speed']*(0.01*3.6*0.62137) #mph
traj17['acceleration']=traj17['acceleration']*(0.001) 
traj17 = traj17[(traj17.speed > 5)]


fig, ax1 = plt.subplots(figsize=(8, 6))
sns.set_style("ticks") 
sns.distplot(traj08['speed'], hist = False, kde = True,kde_kws = {"color": "#2980B9",'lw': 2},label="08")
sns.distplot(traj12['speed'], hist = False, kde = True,kde_kws = {"color": "#FE8E2A",'lw': 2},label="12")
sns.distplot(traj17['speed'], hist = False, kde = True,kde_kws = {"color": "#28B463",'lw': 2},label="17")
plt.xlabel("Speed (mph)",fontsize = 14)
plt.ylabel("Density",fontsize = 14)
ax1.set(xlim=(0, 75))
plt.setp(ax1.get_xticklabels(), fontsize = 14)
plt.setp(ax1.get_yticklabels(), fontsize = 14)
ax1.legend().set_title('Hour')
#plt.title('Route 10G',fontsize = 14)
plt.show()


#figure5 right

path = r'E:/SUMO/RUIXIAO/newChattanooganet/Data/output/figure5right/08'                    
all_files = glob.glob(os.path.join(path, "Route*.csv")) 
speedmean08 = pd.DataFrame()
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(int)
    df['speed']=df['speed']*(0.01*3.6*0.62137) #mph
    speedmean08.loc[0,c]=df.iloc[:,0].mean()
    c=c+1
speedmean08.columns=['10A','10G','16','1','21','33','4','8','9']
speedmean08=speedmean08.T
speedmean08 = speedmean08.reset_index()
speedmean08.columns=['Route','Speed']
speedmean08['Hour'] = "08"

path = r'E:/SUMO/RUIXIAO/newChattanooganet/Data/output/figure5right/12'                    
all_files = glob.glob(os.path.join(path, "Route*.csv")) 
speedmean12 = pd.DataFrame()
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(int)
    df['speed']=df['speed']*(0.01*3.6*0.62137) #mph
    speedmean12.loc[0,c]=df.iloc[:,0].mean()
    c=c+1
speedmean12.columns=['10A','10G','16','1','21','33','4','8','9']
speedmean12=speedmean12.T
speedmean12 = speedmean12.reset_index()
speedmean12.columns=['Route','Speed']
speedmean12['Hour']="12"

path = r'E:/SUMO/RUIXIAO/newChattanooganet/Data/output/figure5right/17'                    
all_files = glob.glob(os.path.join(path, "Route*.csv")) 
speedmean17 = pd.DataFrame()
c=0
for f in all_files:
    df=pd.read_csv(f, usecols=[2]) 
#    df.drop(df.index[0],inplace=True)
    df = df.astype(int)
    df['speed']=df['speed']*(0.01*3.6*0.62137) #mph
    speedmean17.loc[0,c]=df.iloc[:,0].mean()
    c=c+1
speedmean17.columns=['10A','10G','16','1','21','33','4','8','9']
speedmean17=speedmean17.T
speedmean17 = speedmean17.reset_index()
speedmean17.columns=['Route','Speed']
speedmean17['Hour']="17"


speedmean=pd.concat([speedmean08,speedmean12,speedmean17],ignore_index=True)

fig, ax1 = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=speedmean, x="Route", y="Speed", hue="Hour", style="Hour",legend=False)
sns.lineplot(data=speedmean, x="Route", y="Speed", hue="Hour", style="Hour",linewidth = 2)
plt.xlabel("Route",fontsize = 14)
plt.ylabel("Average Speed of Buses(mph)",fontsize = 14)
#ax1.set(xlim=(0, 75))
plt.setp(ax1.get_xticklabels(), fontsize = 14)
plt.setp(ax1.get_yticklabels(), fontsize = 14)
#ax1.legend().set_title('Hour')
#plt.title('Route 10G',fontsize = 14)
plt.show()







