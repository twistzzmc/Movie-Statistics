import matplotlib.pyplot as plt
import numpy as np
import Film
import random
import scipy.stats as stats
import math

"""
μ±σ includes approximately 68% of the observations
μ±2⋅σ includes approximately 95% of the observations
μ±3⋅σ includes almost all of the observations (99.7% to be more precise)
"""


class Stats:
    colors = ['#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF',
              '#FF00FF', '#C0C0C0', '#808080', '#800000', '#808000', '#008000', '#800080',
              '#008080', '#000080']

    @staticmethod
    def plot_film(film):
        percentages = film.stats.get_percentages()

        plt.xlabel('Rating')
        plt.ylabel('Percentage of votes')
        plt.title('{} ({})'.format(film.title, film.year))

        plt.plot([i + 1 for i in range(10)], percentages, 'b--')
        plt.plot([i + 1 for i in range(10)], percentages, 'ro')
        plt.axis([1, 10, 0, 100])

        for i in range(10):
            plt.annotate(str(percentages[i]) + '%', (i + 1, percentages[i] + 5))
        plt.show()

    @staticmethod
    def plot_films(films):
        plt.xlabel('Rating')
        plt.ylabel('Percentage of votes')
        plt.title('Comparing {} movies'.format(len(films)))

        plt.axis([1, 10, 0, 100])

        used_colors = set()
        for film in films:
            color, used_colors = Stats.pick_random_color(used_colors)
            percentages = film.stats.get_percentages()

            plt.plot([i + 1 for i in range(10)], percentages, 'o--',
                     color=color, label='{} ({})'.format(film.title, film.year))

        plt.legend()

        plt.show()

    @staticmethod
    def pick_random_color(used_colors):
        while True:
            color = Stats.colors[random.randint(0, len(Stats.colors) - 1)]
            if color not in used_colors:
                used_colors.add(color)
                return color, used_colors

    @staticmethod
    def plot_normal_distribution(parameter_pairs):
        plt.title('Probability density function')

        for mu, variation, color in parameter_pairs:
            sigma = math.sqrt(variation)
            x = np.linspace(-5, 5, 1000)
            plt.plot(x, stats.norm.pdf(x, mu, sigma), color=color,
                     label='mu={} sigma={}'.format(round(mu, 2), round(variation, 2)))

        plt.legend()
        plt.show()

    @staticmethod
    def plot_normal_distribution_of_film(film):
        percentages = [round(i / 100, 3) for i in film.stats.get_percentages()]

        plt.plot([i + 1 for i in range(10)], percentages, 'o--', color='red',
                 label='{} ({})'.format(film.title, film.year))

        top_y = max(percentages)
        top_x = percentages.index(top_y) + 1

        mu = top_x
        variation = Stats.guess_sigma(mu, top_y, mu, 0.001)
        sigma = math.sqrt(variation)
        x = np.linspace(-5 + mu, 5 + mu, 1000)
        plt.plot(x, stats.norm.pdf(x, mu, sigma), color='blue',
                 label='mu={} sigma={}'.format(round(mu, 2), round(variation, 2)))

        plt.legend()
        plt.show()

    @staticmethod
    def probability_density_function(x, mu, sigma):
        return (1 / (sigma * math.sqrt(2 * math.pi))) * (math.e**((-1 / 2) * ((x - mu) / sigma)**2))

    @staticmethod
    def guess_sigma(x, y, mu, epsilon):
        variation = epsilon

        while True:
            current_y = Stats.probability_density_function(x, mu, math.sqrt(variation))
            next_y = Stats.probability_density_function(x, mu, math.sqrt(variation) + epsilon)

            if abs(y - next_y) < abs(y - current_y):
                variation += epsilon
            else:
                return round(variation, len(str(epsilon).replace('0.', '', 1)))

    @staticmethod
    def plot_year_percentage_of_ranking(films, ranking):
        films.sort(key=lambda x: x.year)
        percentages = [film.stats.get_percentages()[ranking - 1] for film in films]
        years = [film.year for film in films]

        intervals = [(0, 1919)] + [(1920 + 10 * i, 1929 + 10 * i) for i in range(10)] + [(2020, 3000)]
        average_interval_rankings = [(0, 0)] * 12

        j = 0
        for i in range(len(films)):
            if films[i].year <= intervals[j][1]:
                average_interval_rankings[j] = (average_interval_rankings[j][0] + percentages[i], average_interval_rankings[j][1] + 1)
            else:
                j += 1
        intervals = [1915 + i * 10 for i in range(12) if average_interval_rankings[i][1] != 0]
        average_interval_rankings = [round(average[0] / average[1], 3) for average in average_interval_rankings if average[1] != 0]

        plt.plot(years, percentages, 'ro')
        plt.plot(intervals, average_interval_rankings, 'b-')
        plt.show()


if __name__ == "__main__":
    # Film.save_multiple(Film.get_films_from_file('movies/movie_urls.txt'), 'stats_test')
    # Stats.plot_films(Film.load_multiple('movies/stats_test.pickle'))

    # Stats.plot_normal_distribution([(0, 1.0, 'red'), (0, 0.2, 'blue'),
    #                                 (0, 5.0, 'yellow'), (-2, 0.5, 'green')])

    # fs = Film.load_multiple('movies/stats_test.pickle')
    # for f in fs:
        # if f.title == 'Little Women':
        # Stats.plot_normal_distribution_of_film(f)

    f = Film.Films(Film.Film.load_multiple('movies/most_popular_movies.pickle'))
    oldest_films = f.get_movies_sorted_by_age(0, 3)
    newest_films = f.get_movies_sorted_by_age(246)
    Stats.plot_year_percentage_of_ranking(f.films, 1)
