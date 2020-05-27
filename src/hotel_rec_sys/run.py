import sys
sys.path.append('../hotel_rec_sys/feature/')
sys.path.append('../hotel_rec_sys/model/')
sys.path.append('../hotel_rec_sys/config/')

from config import config
import load
import feature_engineering
import sparse_featuring
import widendeep
import deepfm
import xdeepfm
import traintest
import warnings
warnings.filterwarnings("ignore")

#load data and choose number of rows
df = load.load_data(150000)

#Remove rows with the same user_id and item_id and different rating
df = load.remove_duplicate(df)

# Apply feature engineering
df = feature_engineering.extract_week(df,'date_time','click_week')
df = feature_engineering.extract_month_year(df)
df = feature_engineering.add_holiday(df)
df = feature_engineering.log_transform(df,'orig_destination_distance')
#df = feature_engineering.z_score_normalizing(df,'cnt')
df = feature_engineering.create_cluster(df,'user_location_region',config.cluster["user_region_n_cluster"])
df = feature_engineering.create_cluster(df,'user_location_city',config.cluster["user_city_n_cluster"])
df = feature_engineering.extract_family_status(df)

linear_feature_columns,dnn_feature_columns,feature_names = sparse_featuring.simple_pre(df)

train,test,train_model_input,test_model_input = traintest.train_test(linear_feature_columns,dnn_feature_columns,feature_names,df)

# wide and deep
widendeep_result = widendeep.widendeep_model(linear_feature_columns,dnn_feature_columns,train_model_input,train,test_model_input,test)

#DeepFM
deepfm_result = deepfm.deepfm_model(linear_feature_columns,dnn_feature_columns,train_model_input,train,test_model_input,test)

#XDeepFM
xdeepfm_result = xdeepfm.xdeepfm_model(linear_feature_columns,dnn_feature_columns,train_model_input,train,test_model_input,test)

print("Wide and Deep", widendeep_result,"DeepFM", deepfm_result,"XDeepFM", xdeepfm_result, sep='\n')
