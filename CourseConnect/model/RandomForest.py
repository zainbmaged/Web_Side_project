import os
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from CourseConnect.settings import BASE_DIR

def define_label_encoders(all_courses):
    label_encoders = []
    fields = ['Level', 'Language', 'Platform', 'Certificate', 'Duration', 'Category', 'Learning_Type', 'Instructors']
    for field in fields:
        # Collect all unique values for the field
        unique_values = set(getattr(course, field) for course in all_courses)
        # Define and fit label encoder for the field
        label_encoder = LabelEncoder()
        label_encoder.fit(list(unique_values))
        label_encoders.append(label_encoder)
    return label_encoders

def train_random_forest_regressor(reviewed_courses, label_encoders):
    # Collect features and target variable
    features = []
    ratings = []
    fields = ['Level', 'Language', 'Platform', 'Certificate', 'Duration', 'Category', 'Learning_Type', 'Instructors']
    for course in reviewed_courses:
        # Extract features
        feature_vector = [getattr(course, field) for field in fields]
        features.append(feature_vector)
        # Extract target variable
        ratings.append(course.rating)

    # Convert lists to numpy arrays
    X = np.array(features)
    y = np.array(ratings)

    # Apply label encoding to categorical features
    for i, label_encoder in enumerate(label_encoders):
        X[:, i] = label_encoder.transform(X[:, i])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)
    params = {
        "n_estimators": 200,
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1
    }

    # Train the Random Forest regressor
    regressor = RandomForestRegressor(**params, random_state=13)
    regressor.fit(X_train, y_train)

    # Evaluate the regressor
    y_pred = regressor.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return regressor

def predict_top_rated_courses(unrated_courses, regressor, label_encoders, top_n=20):
    # Collect features for unrated courses
    features = []
    fields = ['Level', 'Language', 'Platform', 'Certificate', 'Duration', 'Category', 'Learning_Type', 'Instructors']
    for course in unrated_courses:
        # Extract features
        feature_vector = [getattr(course, field) for field in fields]
        features.append(feature_vector)

    # Convert features to numpy array
    X = np.array(features)

    # Apply label encoding to categorical features
    for i, label_encoder in enumerate(label_encoders):
        # Transform, ignoring unseen labels
        X[:, i] = label_encoder.transform(X[:, i])
        # Handle unseen labels
        unknown_mask = X[:, i] == -1
        if np.any(unknown_mask):
            # Replace unseen labels with a default value or handle them accordingly
            X[unknown_mask, i] = label_encoder.transform(['<unknown>'])[0]

    # Make predictions
    ratings_predicted = regressor.predict(X)

    # Combine predicted ratings with unrated courses
    courses_with_ratings = list(zip(unrated_courses, ratings_predicted))

    # Sort courses based on predicted ratings (descending order)
    courses_with_ratings.sort(key=lambda x: x[1], reverse=True)

    # Get top rated courses with titles
    top_rated_courses_decoded = []
    for course, rating in courses_with_ratings[:top_n]:
        decoded_course = {
            'Title': course.Title,
            'Level': label_encoders[0].inverse_transform([X[0, 0].astype(int)])[0],  
            'Language': label_encoders[1].inverse_transform([X[0, 1].astype(int)])[0],  
            'Rating': course.Rating,
            'Platform': label_encoders[2].inverse_transform([X[0, 2].astype(int)])[0],  
            'Certificate': label_encoders[3].inverse_transform([X[0, 3].astype(int)])[0],  
            'Duration': label_encoders[4].inverse_transform([X[0, 4].astype(int)])[0],  
            'Category': label_encoders[5].inverse_transform([X[0, 5].astype(int)])[0],  
            'Learning_Type': label_encoders[6].inverse_transform([X[0, 6].astype(int)])[0],  
            'Instructors': label_encoders[7].inverse_transform([X[0, 7].astype(int)])[0],  
            'Predicted Rating': rating
        }
        top_rated_courses_decoded.append(decoded_course)

    return top_rated_courses_decoded