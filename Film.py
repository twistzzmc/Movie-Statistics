import urllib.request
import re
import pickle
import time
import os


class Rating:
    def __init__(self, rating, percentage, votes):
        self.rating = rating
        self.percentage = percentage
        self.votes = votes

    def __repr__(self):
        return 'Rating {} - {}% - {}'.format(self.rating, self.percentage, self.votes)


class FilmRatings:
    def __init__(self, url):
        votes_sum, weighted_average, total_votes, percentages, ratings = FilmRatings._get_ratings(url)

        if votes_sum is not None:
            self.ratings = [Rating(ratings[i], percentages[i], total_votes[i]) for i in range(10)]
            self.votes_sum = votes_sum
            self.weighted_average = weighted_average
        else:
            self.ratings = None
            self.votes_sum = None
            self.weighted_average = None

    def __repr__(self):
        if self.votes_sum is not None:
            ratings = ''
            for rating in self.ratings:
                ratings += str(rating) + '\n'
            return 'Total votes - {}, Weighted average - {}/10\n\n{}'.format(self.votes_sum, self.weighted_average, ratings)
        else:
            return 'Ratings are not available for this title.'

    def get_percentages(self):
        percentages = []
        for rating in self.ratings:
            percentages.append(rating.percentage)
        percentages.reverse()

        return percentages

    def get_votes(self):
        votes = []
        for rating in self.ratings:
            votes.append(rating.votes)
        votes.reverse()

        return votes

    @staticmethod
    def _get_ratings(url):
        page_text = Film.open_url(url)

        if page_text.find("<div class=\"sectionHeading\">No Ratings Available</div>") != -1:
            return None, None, None, None, None

        page_text = page_text[page_text.find('allText'):]
        page_text = page_text[:page_text.find('</table')]

        total_votes = re.findall(r'leftAligned\">(.*?)</div', page_text)
        percentage_of_votes = re.findall(r'&nbsp;\n(.*?)<', page_text, re.DOTALL)
        ratings = re.findall(r'rightAligned\">(.*?)<', page_text)
        votes_sum = re.findall(r'allText\">(.*?)IMDb', page_text, re.DOTALL)
        weighted_average = re.findall(r'weighted average</a> vote of(.*?)/', page_text)

        total_votes.pop(0)
        ratings.pop(0)

        for i in range(10):
            if int(total_votes[i].replace(',', '')) == 0:
                percentage_of_votes.insert(i, '0')

        for i in range(10):
            total_votes[i] = int(total_votes[i].replace(',', ''))
            percentage_of_votes[i] = float(percentage_of_votes[i].strip(' ').strip('\n').strip('%'))
            ratings[i] = int(ratings[i])

        votes_sum = int(votes_sum[0].strip('\n').strip(' ').replace(',', ''))
        weighted_average = float(weighted_average[0].strip(' '))

        return votes_sum, weighted_average, total_votes, percentage_of_votes, ratings


class Film:
    def __init__(self, url):
        title, year = self._handle_url(url)

        self.title = title
        self.year = year
        self.url = url
        self.stats = FilmRatings(self._get_stats_url())

    def __repr__(self):
        return '{} {} \n{}\n{}'.format(self.title, '(' + str(self.year) + ')' if self.year is not None else '', self.url, self.stats)

    def __eq__(self, other):
        return self.title == other.title and self.year == other.year

    def __hash__(self):
        return hash((self.title, self.year))

    @staticmethod
    def open_url(url):
        while True:
            try:
                page_text = urllib.request.urlopen(url).read().decode('utf-8')
                break
            except Exception:
                print('Connection failed! Trying again...')
                pass
        return page_text

    @staticmethod
    def _handle_url(url):
        page_text = Film.open_url(url)

        title_and_year = re.findall(r'<meta property=\'og:title\' content=\"(.*?) - IMDb\" />', page_text)

        title = re.findall(r'(.*?)\(', title_and_year[0])[0].strip(' ') if title_and_year[0].find('(') != -1 else title_and_year[0]
        year = int(re.findall(r'\((.*?)\)', title_and_year[0])[0]) if title_and_year[0].find('(') != -1 else None

        return title, year

    def _get_stats_url(self):
        url = self.url.replace('?', 'ratings?')
        url = url.replace('=*', 'tt_ov_rt')
        return url

    @staticmethod
    def _get_movies_from_list(url):
        page_text = Film.open_url(url)
        # page_text = page_text[page_text.find("<td class=\"titleColumn\">"):]
        links = re.findall(r'<a href=\"(.*?)\"', page_text, re.DOTALL)

        for i in range(len(links) - 1, -1, -1):
            if links[i].find('title') == -1 or len(re.findall(r'/title/tt(.*?)/', links[i])) == 0:
                links.pop(i)
            else:
                links[i] = "https://www.imdb.com/" + links[i] + "?ref_=ttls_li_tt"

        new_links = []
        for i in range(len(links)):
            if i % 2 == 0:
                new_links.append(links[i])

        for link in new_links:
            print(link)

        return new_links

    @staticmethod
    def _get_movies_from_category(url):
        page_text = Film.open_url(url)
        page_text = page_text[page_text.find("<div class=\"lister-item-image float-left\">"):]
        links = re.findall(r'<a href=\"(.*?)\"', page_text)

        for i in range(len(links) - 1, -1, -1):
            if len(re.findall(r'/title/tt(.*?)/', links[i])) == 0 or links[i].find('vote?v=X;k=') != -1:
                links.pop(i)
            else:
                links[i] = "https://www.imdb.com/" + links[i] + "?ref_=ttls_li_tt"

        new_links_set = set()
        new_links_list = list()
        for i in range(len(links)):
            if links[i] not in new_links_set and links[i].find('plotsummary') == - 1:
                new_links_set.add(links[i])
                new_links_list.append(links[i])

        # for link in new_links_list:
        #     print(link)
        print(links)

        return new_links_list

    @staticmethod
    def get_movies_from_ranking(url, n=-1):
        film_urls = Film._get_movies_from_list(url)
        films_handled = []
        for i in range(len(film_urls)):
            if n != -1 and i >= n:
                break
            print('Handling - ' + film_urls[i], end='')

            time_start = time.time()
            films_handled.append(Film(film_urls[i]))
            time_end = time.time()

            films_left = len(film_urls) - i - 1 if n == -1 else n - i - 1
            print(' - Success, films left - {} - Took {}s'.format(films_left, round(time_end - time_start, 2)))

        return films_handled

    @staticmethod
    def save_movies_from_genre(genre, start=1, end=51, path='genre_films', min_num_votes=25000, sorting='user_rating', order='desc'):
        url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=' + str(min_num_votes) + \
              ',&genres=' + genre + '&sort=' + sorting + ',' + order + '&start=' + str(start) + '&ref_=adv_prv'

        total_titles = int(re.findall(r'of (.*?) titles.</span>', Film.open_url(url))[0].replace(',', ''))

        if end == -1 or end > total_titles + 1:
            end = total_titles + 1

        print('Searching titles under url:\n' + url)
        print('Total titles found - {}, Starting search from {} title, Total titles to handle {}\n\n'.format(total_titles, start, end - start))

        total_films_left = end - start
        while start < end:
            page = int((start - 1) / 50 + 1)
            print('Getting links from page {}... Total films left {}...'.format(page, total_films_left))
            links = Film._get_movies_from_category(url)
            if end - start < 50:
                links = links[:end - start]
            films_handled = []

            print('\nHandling links from page {}, index of first movie - {}...'.format(page, start))
            for j in range(len(links)):
                print('Handling - ' + links[j], end='')

                time_start = time.time()
                films_handled.append(Film(links[j]))
                time_end = time.time()

                films_left = len(links) - j - 1
                print(' - Success, films left - {} - Took {}s'.format(films_left, round(time_end - time_start, 2)))

                if start >= end:
                    break
                else:
                    start += 1

            start = int(re.findall(r'start=(.*?)&', url)[0]) + 50
            total_films_left -= 50
            url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=' + str(min_num_votes) + \
                  ',&genres=' + genre + '&sort=' + sorting + ',' + order + '&start=' + str(start) + '&ref_=adv_prv'

            if os.path.isfile(path):
                print('Loading films already handled...')
                already_handled_films = Film.load_multiple(path) + films_handled
            else:
                already_handled_films = [] + films_handled

            print('Saving films handled thus far...\n\n')
            Film.save_multiple(Film.get_unique_films(already_handled_films), path)

        print('Films saved successfully under \"{}\" name'.format(path))

    @staticmethod
    def get_urls_from_genre(genre, start=1, end=51, path='genre_films', min_num_votes=25000, sorting='user_rating', order='desc'):
        url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=' + str(min_num_votes) + \
              ',&genres=' + genre + '&sort=' + sorting + ',' + order + '&start=' + str(start) + '&ref_=adv_prv'

        total_titles = int(re.findall(r'of (.*?) titles.</span>', Film.open_url(url))[0].replace(',', ''))

        if end == -1 or end > total_titles + 1:
            end = total_titles + 1

        print('Searching titles under url:\n' + url)
        print('Total titles found - {}, Starting search from {} title, Total titles to handle {}\n'.format(total_titles, start, end - start))

        all_urls = set()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    all_urls.add(line.strip('\n'))
        except FileNotFoundError:
            pass

        total_films_left = end - start
        file = open(path, 'a')
        while start < end:
            page = int((start - 1) / 50 + 1)
            print('\nGetting links from page {}... Total films left {}...\nurl - {}'.format(page, total_films_left, url))
            links = Film._get_movies_from_category(url)
            if end - start < 50:
                links = links[:end - start]

            print('Handling links from page {}, index of first movie - {}...'.format(page, start))
            for j in range(len(links)):
                if links[j] not in all_urls:
                    file.write(links[j] + '\n')

            start = int(re.findall(r'start=(.*?)&', url)[0]) + 50
            total_films_left -= 50
            url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=' + str(min_num_votes) + \
                  ',&genres=' + genre + '&sort=' + sorting + ',' + order + '&start=' + str(start) + '&ref_=adv_prv'

        file.close()

    def save(self):
        with open(self.title + '.pickle', 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    @staticmethod
    def save_multiple(films_to_save, path='films'):
        with open(path, 'wb') as pickle_file:
            pickle.dump(films_to_save, pickle_file)

    @staticmethod
    def load(path):
        with open(path, 'rb') as pickle_file:
            loaded_film = pickle.load(pickle_file)
        return loaded_film

    @staticmethod
    def load_multiple(path):
        with open(path, 'rb') as pickle_file:
            loaded_films = pickle.load(pickle_file)
        return loaded_films

    @staticmethod
    def get_films_from_file(path):
        file = open(path, encoding='utf-8')
        films = []

        for line in file:
            films.append(Film(line.strip('\n')))

        return films

    @staticmethod
    def get_unique_films(films):
        films_set = set()
        for i in range(len(films) - 1, -1, -1):
            if films[i] not in films_set:
                films_set.add(films[i])
            else:
                films.pop(i)
        return films

    @staticmethod
    def save_to_all_movies(path, all_movies_path='movies/all_movies.pickle'):
        films = Film.load_multiple(path)
        all_films = Film.load_multiple(all_movies_path)

        all_films_set = set(all_films)
        movies_to_save = [film for film in films if film not in all_films_set]

        new_all_films = all_films + Film.get_unique_films(movies_to_save)
        Film.save_multiple(new_all_films, all_movies_path)

    @staticmethod
    def save_movies_not_already_saved_from_urls_in_file(path, path_with_pickled_films):
        if os.path.isfile(path_with_pickled_films):
            links_set = set([film.url.strip('\n') for film in Film.load_multiple(path_with_pickled_films)])
        else:
            links_set = set()

        with open(path, "r+") as f, open(path[:path.find('.')] + '_copy.txt', 'w', buffering=1) as f_copy:
            new_f = f.readlines()
            f.seek(0)
            for i, line in enumerate(new_f):
                if line.strip('\n') not in links_set:
                    print("Handling movie - {} - ".format(line.strip('\n')), end='')
                    time_start = time.time()
                    film = [Film(line.strip('\n'))]
                    time_end = time.time()
                    print("success - took {}, films left - {}, Saving movie"
                          .format(round(time_end - time_start, 2), len(new_f) - i - 1), end='')

                    try:
                        already_saved = Film.load_multiple(path_with_pickled_films)
                        Film.save_multiple(already_saved + film, path_with_pickled_films)
                    except FileNotFoundError:
                        Film.save_multiple(film, path_with_pickled_films)

                    print(' - success, Deleting line - ', end='')
                    f_copy.write(line)
                    print(' - success')
                else:
                    f_copy.write(line)
                    print('Film - {} - already in this .pickle file'.format(line.strip('\n')))

        os.remove(path[:path.find('.')] + '_copy.txt')

    @staticmethod
    def clean_urls(path):
        if path.find('.pickle') != -1:
            raise Exception('Wrong file \".pickle\"')

        delete_if_found = ['synopsis']

        with open(path, 'r') as f:
            lines = f.readlines()
        with open(path, 'w') as f:
            for line in lines:
                write = True
                for el in delete_if_found:
                    if line.find(el) != -1:
                        write = False
                if write:
                    f.write(line)

    @staticmethod
    def delete_already_handled_urls(path, path_copy):
        if path.find('.pickle') != -1 or path_copy.find('.pickle') != -1:
            raise Exception('Wrong file \".pickle\"')

        with open(path, 'r') as f, open(path_copy, 'r') as f_copy:
            lines = [line.strip('\n') for line in f.readlines()]
            lines_copy_set = set([line.strip('\n') for line in f_copy.readlines()])

        with open(path, 'w') as f:
            for line in lines:
                if line not in lines_copy_set:
                    f.write(line + "\n")

        os.remove(path_copy)

    @staticmethod
    def common_films(films1, films2):
        films1_set = set(films1)
        common_films = []

        for film in films2:
            if film in films1_set:
                common_films.append(film)

        return common_films

    @staticmethod
    def search_by_url(films, url):
        for film in films:
            if film.url == url:
                return film

    @staticmethod
    def print_dependencies_between_film_files(files, types):
        films = [Film.load_multiple(file) for file in files]

        for i, group in enumerate(films):
            print('Total {} movies - {}'.format(types[i], len(group)))
        print()

        for i in range(len(films)):
            for j in range(len(films)):
                if i != j:
                    print('Total {} movies {} - common with {} - {}'.format(types[i], len(films[i]), types[j], len(Film.common_films(films[i], films[j]))))
            print()


class Filter:
    @staticmethod
    def total_votes(films, min_total_votes, max_total_votes=-1):
        matches = []
        for film in films:
            if film.stats.votes_sum > min_total_votes and (max_total_votes == -1 or film.stats.votes_sum < max_total_votes):
                matches.append(film)
        return matches
