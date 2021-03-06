from Film import Film
from Stats import Stats
from Film import Filter


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

    """
    Efficient way of getting large quantities of films:
    
        Film.get_urls_from_genre(genre, start=1, end=51, path='genre_films', min_num_votes=25000, sorting='user_rating', order='desc')
            Were all attributes are the same as explained in comment above. The difference is that it gets all the urls
            and instead of creating Film instances it puts them into file (text) specified in path.
            
        Film.clean_urls(path)
            Were path is path to the text file with urls (e.g. given by previous method).
            It removes all bad urls (with some garbage in them, not for the main site of the film).
            
        Film.save_movies_not_already_saved_from_urls_in_file(path, path_with_pickled_films)
            Were path is path to the text file with urls and path_with_pickled_films is path to .pickle file in which
            you wish the save the films. It takes all the urls from file, creates an Film instance with them and save it
            to the specified .pickle file.
            
        If everything goes without an error your file with urls will end up empty.
        
        However if an error occurs additional text file under " path[:path.find('.')] + '_copy.txt' " 
        (e.g. if path='movies/urls.txt' then new file='movies/urls_copy.txt') with all urls that were
        successfully saved. The file under 'path' is not changed. And you should proceed as follows:
            
            Film.delete_already_handled_urls(path, path_copy)
                Were path is the path for original file with urls and path_copy is the path for created file.
                It deletes all the already handled urls from the original file and deletes the copy.
                
            Go back to - Film.save_movies_not_already_saved_from_urls_in_file(path, path_with_pickled_films)
            And do until no error occurs at which point the url file is empty.
    """
    most_popular_movies = "https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=GK4AXVJZ58WM5RH6GWF9&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_2"
    top_rated_movies = "https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=9VQV8P7PPVQ6WSZX5943&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_3"

    film_files = ['movies/' + movie_type + '.pickle' for movie_type in ['all_movies', 'most_popular_movies', 'action_movies', 'romance_movies', 'war_movies']]
    film_types = ['all', 'most popular', 'action', 'romance', 'war']

    # Film.delete_already_handled_urls('movies/thriller_movies_urls.txt', 'movies/thriller_movies_urls_copy.txt')
    # Film.get_urls_from_genre('thriller', 1, -1, path='thriller_movies_urls.txt')
    # Film.save_movies_not_already_saved_from_urls_in_file('movies/thriller_movies_urls.txt', film_files[0])
    Stats.correlation_between_year_and_average_vote(Filter.total_votes(Film.load_multiple(film_files[0]), 0, 10000))
    Stats.plot_averaged_films_rankings_votes_distribution(Filter.total_votes(Film.load_multiple(film_files[0]), 0, 10000))
    Stats.correlation_between_number_of_votes_and_average_vote(Filter.total_votes(Film.load_multiple(film_files[0]), 0, 10000))
