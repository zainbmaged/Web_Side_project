import pickle

def get_recommendations(courses_names):
    if(len(courses_names) == 0):
        return "None"
    # Load the DataFrame from the file using pickle
    with open('df_pickle', 'rb') as f:
        similarity_df = pickle.load(f)
    
    num_courses = len(courses_names)
    recommendations_per_course = 20 // num_courses  # Integer division to distribute 
    all_similar_courses = []
    for course_name in courses_names:
        similarity_score = similarity_df.loc[course_name]
        similarity_score = list(enumerate(similarity_score))
        
        # Sort the courses based on similarity score
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        
        # Get the top 5 similar courses (excluding the input course itself)
        top_5_similar_courses = similarity_score[1:recommendations_per_course+1]  # Exclude the input course itself
        
        # Extract the indices of the similar courses
        similar_course_indices = [x[0] for x in top_5_similar_courses]
        
        # Get the titles of the similar courses
        similar_course_titles = similarity_df.iloc[similar_course_indices].index.tolist()
        
        all_similar_courses.extend(similar_course_titles)
    
    return all_similar_courses
