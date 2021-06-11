def encode_df(df):
    # Encode Genre
    genre_values = df['Genre'].value_counts().keys().tolist()
    genre_list = []
    for each in df.Genre:
        genre_list.append(genre_values.index(each))
    df["Genre_encoding"] = genre_list
    # Encode Publisher
    publisher_values = df['Publisher'].value_counts().keys().tolist()
    publisher_list = []
    for each in df.Publisher:
        publisher_list.append(publisher_values.index(each))
    df["Publisher Encoding"] = publisher_list
    # Encode Platform
    platform_values = df['Platform'].value_counts().keys().tolist()
    platform_list = []
    for each in df.Platform:
        platform_list.append(platform_values.index(each))
    df["Platform Encoding"] = platform_list
    publisher_values = df['Publisher'].value_counts().keys().tolist()
    return df
