from Film import Film


if __name__ == "__main__":
    most_popular_movies = "https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=GK4AXVJZ58WM5RH6GWF9&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_2"
    top_rated_movies = "https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=9VQV8P7PPVQ6WSZX5943&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_ql_3"
    action_movies = "https://www.imdb.com/search/title/?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=7NEKCG0JCHH310HJH8DY&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_1"
    # films = Film.get_movies_from_ranking(action_movies)
    # Film.save_multiple(films, 'action_movies')

    films = Film.load_multiple('action_movies.pickle')
    print(len(films))
    for film in films:
        print(film)

    # Film.save_movies_from_genre(action_movies, 20, 'action_movies')
