def combine_columns(df):
    for col in ['title', 'company_profile', 'description', 'requirements', 'benefits']:
        df[col] = df.get(col, "")
    df['text'] = (df['title'].fillna('') + ' ' +
                  df['company_profile'].fillna('') + ' ' +
                  df['description'].fillna('') + ' ' +
                  df['requirements'].fillna('') + ' ' +
                  df['benefits'].fillna('')).str.lower().str.strip()
    return df
