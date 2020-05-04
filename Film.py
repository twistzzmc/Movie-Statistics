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

    @staticmethod
    def _get_ratings(url):
        page_text = urllib.request.urlopen(url).read().decode('utf-8')
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
            total_votes[i] = int(total_votes[i].replace(',', ''))
            percentage_of_votes[i] = percentage_of_votes[i].strip(' ')
            percentage_of_votes[i] = percentage_of_votes[i].strip('\n')
            percentage_of_votes[i] = float(percentage_of_votes[i].strip('%'))
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

    @staticmethod
    def _handle_url(url):
        page_text = urllib.request.urlopen(url).read().decode('utf-8')
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
        page_text = urllib.request.urlopen(url).read().decode('utf-8')
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
        page_text = urllib.request.urlopen(url).read().decode('utf-8')
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
            if links[i] not in new_links_set:
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

        total_titles = int(re.findall(r'of (.*?) titles.</span>', urllib.request.urlopen(url).read().decode('utf-8'))[0].replace(',', ''))

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

            print('\nHandling links from page {}...'.format(page))
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
            url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=&sort=user_rating,desc&start=' + str(start) + '&ref_=adv_prv'

            if os.path.isfile(path + '.pickle'):
                print('Loading films already handled...')
                already_handled_films = Film.load_multiple(path + '.pickle') + films_handled
            else:
                already_handled_films = [] + films_handled

            print('Saving films handled thus far...\n\n')
            Film.save_multiple(already_handled_films, path)

        print('Films saved successfully under \"{}\" name'.format(path + '.pickle'))

    def save(self):
        with open(self.title + '.pickle', 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    @staticmethod
    def save_multiple(films_to_save, path='films'):
        with open(path + '.pickle', 'wb') as pickle_file:
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
