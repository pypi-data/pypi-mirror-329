import pandas as pd
import numpy as np
import statistics

class TDR():
  def run(self, data, round_level = 3):
    """
    This function is a topological dimensionality reduction algorithm.

    :param df:
    :return numpy array [index of important column from original data, importance level]:
    """

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    t_data, _ = self.transform(data, round_level)
    return self.core(t_data)

  def core(self, t_data, addID = True):
    """
    If dataframe have not ID column addID is must True.

    You can select important columns according to their importance level.

    This function is a topological dimensionality reduction algorithm.

    :param transformed df, addID=True:
    :return numpy array [index of important column from original data, importance level]:
    """
    if addID:
    	t_data.insert(0,"ID",np.arange(1,t_data.shape[0]+1))

    ##Initialize-0
    ds0=t_data.shape[0]
    ds1=t_data.shape[1]

    df_y=t_data.iloc[:,-1].values
    df_0=t_data.iloc[:,0].values

    IC=[] #important column and importance level
    BaseRla=set()
    BaseB=set()
    X=set()
    cl_lA = [list(range(1, ds1-1))] + [list(range(1, ds1-1))[:i] + list(range(1, ds1-1))[i+1:] for i in range(ds1-2)]
    ##Initialize-0

    ##Shine Examples
    for i in range(ds0):
      if int(df_y[i]) == 0:
        X.add(df_0[i])
    ##Shine Examples

    for p in range(ds1-1):

      ##Initialize-1
      Rla=[]
      B=[]
      U_R = []
      U = list(df_0)
      cl_l=cl_lA[p]
      ##Initialize-1
      #print(t_data.columns[p])
      #print(cl_l)
      

      ##Equivalence Classes
      df_s=t_data.iloc[:,cl_l].values
      while U:
        i = U[0]
        chc = [i]
        for j in U:
            if np.array_equal(df_s[i - 1], df_s[j - 1]) and i != j:
                chc.append(j)
        U = [x for x in U if x not in chc]
        U_R.append(list(chc))
      ##Equivalence Classes
      #print(U_R)

      ##Lower Approximation-Border
      for i in U_R:
        for j in i:
          if set(i).issubset(X):
            Rla.append(j)
          elif not set(i).isdisjoint(X):
            B.append(j)
      ##Lower Approximation-Border

      """   	
      print("Examples",U)
      print("Shine Examples",X)
      print("Equivalence Classes",U_R)
      print("Lower Approximation",Rla)
      print("Border",B)
      print("*"*75)
      """

      if p>0:
        if not (BaseRla==set(Rla) and BaseB==set(B)):
            IC.append([p-1, len(BaseB.symmetric_difference(set(B)))])
      else:
        BaseRla=set(Rla)
        BaseB=set(B)

    return np.array(IC)

  def transform(self, data, round_level = 3):
    """
    This function convert data into categories (1,2,3,4,...) based on standard deviation.

    If the convert is not correct and the decimal part of your data is high, you can increase the round_level variable.

    If there is an ID column in the dataset, please cancel this column.

    :param df:
    :return convert df and transform dict:
    """
    t_data = data.copy()
    transform_dict = {}

    for i in range(t_data.shape[1]-1):
      # Convert the column to numeric type, coercing errors to NaN
      used_class_list = [] # To collect used classes
      t_data.iloc[:, i] = pd.to_numeric(t_data.iloc[:, i], errors='coerce') # Convert the i-th column of self.t_data to numeric values, setting non-convertible entries to NaN
      transform_dict[i] = {} # Information about which values ​​are assigned to which classes

      c = statistics.stdev(t_data.iloc[:,i].dropna())
      d = 1

      while len(used_class_list) != (t_data.iloc[:,i].shape[0] - t_data.iloc[:, i].isna().sum()):
        try:
          v = round(np.nanmax([t for j,t in enumerate(t_data.iloc[:,i]) if (j not in used_class_list)]) - c, round_level) # normal:3

          #print(v,c,(df.iloc[:,i] > v).sum())

          # Converts class
          for j, k in enumerate(t_data.iloc[:,i]):

            if (j not in used_class_list) and (k>=v):
              t_data.iloc[j,i] = d
              transform_dict[i][d] = v
              used_class_list.append(j)

          d += 1
        except Exception as e:
          print("Rise an Error: ",e)
          break
    return t_data, transform_dict