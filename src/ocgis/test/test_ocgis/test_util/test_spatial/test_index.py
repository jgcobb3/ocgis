import itertools

import numpy as np
from shapely import wkt
from shapely.geometry.geo import mapping
from shapely.geometry.point import Point

from ocgis.test.base import TestBase
from ocgis.util.spatial.index import SpatialIndex


class TestSpatialIndex(TestBase):
    @property
    def geom_michigan(self):
        wkt_txt = 'MULTIPOLYGON(((-88.497527 48.173795,-88.625327 48.033167,-88.901547 47.960248,-89.028622 47.850655,-89.139885 47.824076,-89.192916 47.844613,-89.201787 47.883857,-89.156099 47.939228,-88.497527 48.173795)),((-88.500681 47.290180,-88.437901 47.355896,-88.211392 47.447835,-87.788120 47.470793,-87.704383 47.415950,-87.737510 47.393024,-87.917042 47.358007,-88.222279 47.200752,-88.412843 46.988094,-88.470664 47.111472,-88.594262 47.134765,-88.595632 47.243593,-88.500681 47.290180)),((-85.859844 45.969469,-85.914955 45.957978,-85.917104 45.918192,-86.067891 45.964210,-86.259319 45.946929,-86.315638 45.905682,-86.343795 45.834396,-86.458275 45.762747,-86.529390 45.748961,-86.522010 45.724094,-86.576124 45.710174,-86.629784 45.621233,-86.685053 45.650048,-86.696919 45.692511,-86.584735 45.813879,-86.761469 45.826067,-86.901624 45.714778,-87.123759 45.696246,-87.260707 45.554802,-87.332227 45.423942,-87.583864 45.162733,-87.592514 45.108501,-87.672814 45.140672,-87.729669 45.176604,-87.736200 45.199072,-87.721628 45.211672,-87.719668 45.236771,-87.705142 45.247086,-87.704471 45.272205,-87.645362 45.348169,-87.643684 45.361856,-87.689598 45.391269,-87.760038 45.352897,-87.828008 45.358321,-87.841282 45.346149,-87.862096 45.370165,-87.868535 45.372072,-87.873974 45.362085,-87.883610 45.365854,-87.849531 45.406117,-87.860267 45.445098,-87.813614 45.466460,-87.789385 45.499067,-87.805141 45.544525,-87.828602 45.568591,-87.786312 45.568519,-87.775075 45.600387,-87.776045 45.613200,-87.819938 45.654450,-87.817054 45.665390,-87.780945 45.675915,-87.777473 45.684101,-87.801156 45.701324,-87.801553 45.711391,-87.842362 45.722418,-87.873629 45.750699,-87.969179 45.766448,-87.990070 45.795046,-88.051639 45.786112,-88.088734 45.791532,-88.129949 45.819402,-88.121786 45.834878,-88.065421 45.873642,-88.095764 45.891803,-88.093850 45.920615,-88.111390 45.926287,-88.150438 45.936293,-88.180194 45.953516,-88.214992 45.947901,-88.257168 45.967055,-88.299152 45.961944,-88.321323 45.966712,-88.369938 45.994587,-88.403522 45.983422,-88.454319 46.000760,-88.483814 45.999151,-88.494083 46.012960,-88.515613 46.018609,-88.548358 46.019300,-88.575357 46.008959,-88.597536 46.015516,-88.615502 45.994120,-88.643669 45.993388,-88.677384 46.020144,-88.703605 46.018923,-88.726409 46.029581,-88.773017 46.021147,-88.777480 46.032614,-88.793815 46.036360,-88.804397 46.026804,-88.925195 46.073601,-88.985301 46.100391,-89.099806 46.145642,-89.925136 46.304025,-90.111659 46.340429,-90.115177 46.365155,-90.141797 46.393899,-90.161391 46.442380,-90.211526 46.506295,-90.258401 46.508789,-90.269785 46.522480,-90.300181 46.525051,-90.302393 46.544296,-90.313708 46.551563,-90.385525 46.539657,-90.408200 46.568610,-90.018864 46.678633,-89.886252 46.768935,-89.791244 46.824713,-89.386718 46.850208,-89.214592 46.923378,-89.125187 46.996606,-88.994875 46.997103,-88.929688 47.030926,-88.884832 47.104554,-88.629500 47.225812,-88.618104 47.131114,-88.511215 47.106506,-88.512995 47.032589,-88.441164 46.990734,-88.445964 46.928304,-88.476523 46.855151,-88.446617 46.799396,-88.177827 46.945890,-88.189188 46.900958,-88.036685 46.911865,-87.900654 46.909761,-87.663766 46.836851,-87.371539 46.507991,-87.110679 46.501473,-87.006402 46.536293,-86.871382 46.444359,-86.759495 46.486631,-86.638220 46.422263,-86.462392 46.561085,-86.148109 46.673053,-86.096739 46.655268,-85.857536 46.694815,-85.503850 46.674174,-85.230094 46.756785,-84.954759 46.770951,-85.026971 46.694339,-85.018975 46.549024,-85.051655 46.505576,-85.016639 46.476444,-84.931320 46.487843,-84.803653 46.444054,-84.629815 46.482943,-84.572667 46.407926,-84.415967 46.480658,-84.311614 46.488669,-84.181646 46.248720,-84.273134 46.207309,-84.247031 46.171447,-84.119735 46.176108,-84.029578 46.128943,-84.061981 46.094470,-83.989501 46.025985,-83.901952 46.005902,-83.906460 45.960239,-84.113272 45.978538,-84.354485 45.999190,-84.501635 45.978342,-84.616845 46.038230,-84.689022 46.035918,-84.731732 45.855679,-84.851100 45.890636,-85.061629 46.024751,-85.378243 46.100047,-85.509546 46.101911,-85.655381 45.972870,-85.859844 45.969469)),((-83.854680 46.014031,-83.801105 45.988412,-83.756420 46.027338,-83.673592 46.036192,-83.680314 46.071794,-83.732448 46.084108,-83.649887 46.103971,-83.589498 46.088518,-83.533991 46.011790,-83.473189 45.987547,-83.516159 45.925714,-83.579813 45.917501,-83.629705 45.953596,-83.804881 45.936764,-83.852810 45.997449,-83.885891 45.970852,-83.854680 46.014031)),((-86.834829 41.765504,-86.617592 41.907448,-86.498833 42.126446,-86.374278 42.249421,-86.284980 42.422324,-86.217854 42.774825,-86.273837 43.121045,-86.463201 43.475166,-86.541301 43.663187,-86.447811 43.772665,-86.404345 43.766642,-86.434101 43.781458,-86.428814 43.820123,-86.459548 43.950184,-86.438147 43.945592,-86.518602 44.053619,-86.386423 44.183204,-86.271954 44.351228,-86.238038 44.522273,-86.258627 44.700731,-86.108484 44.734442,-86.082918 44.777929,-86.097964 44.850612,-86.067454 44.898257,-85.795756 44.985974,-85.610215 45.196527,-85.565514 45.180560,-85.653006 44.958362,-85.638039 44.778435,-85.526081 44.763162,-85.451351 44.860540,-85.384869 45.010603,-85.390244 45.211593,-85.373253 45.273541,-85.305475 45.320383,-85.092862 45.370225,-84.985893 45.373178,-84.921674 45.409899,-85.081815 45.464650,-85.120447 45.569779,-85.078019 45.630185,-84.983412 45.683713,-84.972038 45.737745,-84.724186 45.780304,-84.465275 45.653637,-84.321458 45.665607,-84.205560 45.630905,-84.135229 45.571343,-84.105907 45.498749,-83.922892 45.491773,-83.782809 45.409449,-83.712318 45.412394,-83.592363 45.349502,-83.495832 45.360802,-83.489598 45.328937,-83.394019 45.272907,-83.420761 45.257182,-83.398695 45.213641,-83.312707 45.098620,-83.444441 45.052773,-83.433972 45.011128,-83.464903 44.997883,-83.429355 44.926297,-83.319724 44.860646,-83.280812 44.703183,-83.320036 44.515460,-83.356963 44.335133,-83.529150 44.261274,-83.568237 44.170118,-83.598404 44.070493,-83.704802 43.997165,-83.873615 43.962842,-83.918376 43.916997,-83.938121 43.698283,-83.699164 43.599642,-83.654615 43.607420,-83.530909 43.725943,-83.494248 43.702841,-83.466408 43.745740,-83.367163 43.844452,-83.326026 43.940459,-82.940154 44.069959,-82.805978 44.033564,-82.727902 43.972506,-82.618487 43.787866,-82.605738 43.694568,-82.503820 43.172253,-82.419836 42.972465,-82.471952 42.898682,-82.473238 42.762896,-82.518179 42.634052,-82.645877 42.631728,-82.634015 42.669382,-82.729806 42.681226,-82.820407 42.635794,-82.802361 42.612926,-82.888138 42.495756,-82.874907 42.458067,-82.929389 42.363040,-83.107588 42.292705,-83.193873 42.115749,-83.190066 42.033979,-83.482691 41.725130,-83.763954 41.717042,-83.868639 41.715993,-84.359208 41.708039,-84.384393 41.707150,-84.790377 41.697494,-84.788478 41.760959,-84.826008 41.761875,-85.193140 41.762867,-85.297209 41.763581,-85.659459 41.762627,-85.799227 41.763535,-86.068302 41.764628,-86.234565 41.764864,-86.525181 41.765540,-86.834829 41.765504)))'
        return wkt.loads(wkt_txt)

    @property
    def geom_michigan_point_grid(self):
        n = 10
        bounds = self.geom_michigan.bounds
        x = np.linspace(bounds[2] + 1, bounds[0] - 1, n)
        y = np.linspace(bounds[1] - 1, bounds[3] + 1, n)
        ret = {}
        for ii, (ix, iy) in enumerate(itertools.product(x, y)):
            ret[ii] = Point(ix, iy)
        return ret

    def test_constructor(self):
        SpatialIndex()

    def test_add_polygon(self):
        si = SpatialIndex()
        si.add(1, self.geom_michigan)
        self.assertEqual(tuple(si._index.bounds), self.geom_michigan.bounds)

    def test_add_point(self):
        pt = self.geom_michigan.centroid
        si = SpatialIndex()
        si.add(1, pt)
        self.assertEqual(tuple(si._index.bounds), pt.bounds)

    def test_add_sequence(self):
        si = SpatialIndex()
        ids = [1, 2]
        geoms = [self.geom_michigan, self.geom_michigan]
        si.add(ids, geoms)
        ids = list(si._index.intersection(self.geom_michigan.bounds))
        self.assertEqual([1, 2], ids)

    def test_get_intersection_rtree(self):
        points = self.geom_michigan_point_grid
        si = SpatialIndex()
        ids = points.keys()
        geoms = [points[i] for i in ids]
        si.add(ids, geoms)
        ids = list(si._get_intersection_rtree_(self.geom_michigan))
        self.assertEqual(set(ids), set(
            [12, 13, 14, 15, 16, 17, 22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 36, 37, 42, 43, 44, 45, 46, 47, 52, 53, 54,
             55, 56, 57, 62, 63, 64, 65, 66, 67, 72, 73, 74, 75, 76, 77, 82, 83, 84, 85, 86, 87]))

    def test_iter_intersects(self):
        points = self.geom_michigan_point_grid
        si = SpatialIndex()
        ids = points.keys()
        geoms = [points[i] for i in ids]
        si.add(ids, geoms)
        intersects_ids = list(si.iter_intersects(self.geom_michigan, points))
        self.assertEqual(set(intersects_ids), set([22, 23, 24, 32, 33, 34, 35, 36, 42, 43, 44, 46, 56, 66, 67, 76]))

    def test_keep_touches(self):
        points = self.geom_michigan_point_grid
        si = SpatialIndex()
        ids = points.keys()
        geoms = [points[i] for i in ids]
        si.add(ids, geoms)
        touch_geom = Point(*mapping(self.geom_michigan)['coordinates'][0][0][3])
        si.add(1000, touch_geom)
        points[1000] = touch_geom
        for keep_touches in [True, False]:
            intersects_ids = list(si.iter_intersects(self.geom_michigan, points, keep_touches=keep_touches))
            if keep_touches:
                self.assertIn(1000, intersects_ids)
            else:
                self.assertNotIn(1000, intersects_ids)

    def test_iter_intersects_with_polygon(self):
        polygon = self.geom_michigan[1]
        si = SpatialIndex()
        points = self.geom_michigan_point_grid
        ids = points.keys()
        geoms = [points[i] for i in ids]
        si.add(ids, geoms)
        intersects_ids = list(si.iter_intersects(polygon, points))
        self.assertEqual(intersects_ids, [67])
