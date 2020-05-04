from Film import Film


if __name__ == "__main__":
    """
    For method Film.save_movies_from_genre(genre, start=1, end=51, path='genre_films', min_num_votes=25000, sorting='user_rating', order='desc'):
    
        Example of link used: 
            https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=action&sort=user_rating,desc&start=1&ref_=adv_prv
            
        Pickable features:
            - minimum number of votes (default 25000)
            - genre (must pick)
            - starting position of film (default 1 - first film in list)
            - ending position of film (default 51 - handling of all movies on one page)
            - sort (default user_rating,desc)
            - order (default desc)
            
        Order options:
            - Descending ('desc')
            - Ascending  ('asc')
            
        Sort options:
            - Popularity        ('moviemeter')
            - A-Z               ('alpha)
            - User Rating       ('user_rating')
            - Number of Votes   ('num_votes')
            - US Box Office     ('box_office_gross_us')
            - Runtime           ('runtime')
            - Year              ('year')
            - Release Date      ('release_date')
            
        Genre options:
            - Action        ('action')
            - Adventure     ('adventure')
            - Animation     ('animation')
            - Biography     ('biography')
            - Comedy        ('comedy')
            - Crime         ('crime')
            - Documentary   ('documentary')
            - Drama         ('drama')
            - Family        ('family')
            - Fantasy       ('fantasy')
            - Film-Noir     ('film_noir')
            - History       ('history')
            - Horror        ('horror')
            - Music         ('music')
            - Musical       ('musical')
            - Mystery       ('mystery')
            - Romance       ('romance')
            - Sci-Fi        ('sci_fi')
            - Short         ('short')
            - Sport         ('sport')
            - Thriller      ('thriller')
            - War           ('war')
            - Western       ('western')
    """
    most_popular_movies = "https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=GK4AXVJZ58WM5RH6GWF9&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_2"
    top_rated_movies = "https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=9VQV8P7PPVQ6WSZX5943&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_3"

    # films = Film.get_movies_from_ranking(action_movies)
    # Film.save_multiple(films, 'action_movies')

    # films = Film.load_multiple('action_movies.pickle')
    # print(len(films))
    # for film in films:
    #     print(film)

    Film.save_movies_from_genre('action', 1301, -1, 'movies/test_action_movies')
