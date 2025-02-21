# from umd_api.planet_terp import Search

# search = Search()

# search.search("Raluca")

from umd_api.general import Bus
from umd_api.planet_terp import Professors

bus = Bus()

routes = bus.get_specific_stops(["elk"])

print(routes)

professors = Professors()

professors.get_all_professors(type="ta")