from pluginfiles.plugin import ClusterPluginInterface
import numpy as np
import time


class point:
    value = None
    x = None
    y = None

    def __init__(self, v, x_v, y_v):
        self.value = v
        self.x = x_v
        self.y = y_v


def euclidean_distance(image_point: point, centroid_point: point):
    image_point = np.array((image_point.x, image_point.y))
    x2 = np.array((centroid_point.x, centroid_point.y))
    dist = np.linalg.norm(image_point - x2)
    return dist


def closest_centroid(image_point: point, centroids):
    distances = []
    for centroid_point in centroids:
        dist = euclidean_distance(image_point, centroid_point)
        distances.append(dist)
    closest_centroid_id = np.argmin(distances)
    return closest_centroid_id


def get_mean_centroids(clusters):
    centroids = []
    for centroid_id, cluster in enumerate(clusters):
        v_avg_temp1 = []
        x_avg_temp1 = []
        y_avg_temp1 = []
        for p in cluster:
            v_avg_temp1.append(p.value)
            x_avg_temp1.append(p.x)
            y_avg_temp1.append(p.y)
        v_avg_temp2 = np.array(v_avg_temp1)
        x_avg_temp2 = np.array(x_avg_temp1)
        y_avg_temp2 = np.array(y_avg_temp1)
        cluster_value_mean = np.mean(v_avg_temp2)
        cluster_x_mean = np.mean(x_avg_temp2)
        cluster_y_mean = np.mean(y_avg_temp2)
        new_cluster_point = point(cluster_value_mean, cluster_x_mean, cluster_y_mean)
        centroids.append(new_cluster_point)
    return centroids


class KMeansClustering(ClusterPluginInterface):
    k = None
    max_iterations = None
    centroids = []
    acceptance_value = 2
    image_points_array = None
    segmented_image = None
    col_count = None
    row_count = None
    clusters = None

    def performFilter(self, raw_img, k, max_iterations):
        operation_start_time = time.time()
        self.k = k
        self.centroids = []
        img_data = np.array(raw_img)
        self.segmented_image = img_data.copy()
        self.row_count, self.col_count = self.segmented_image.shape
        self.image_points_array = self.setup_point_array(self)
        self.max_iterations = max_iterations
        self.clusters = [[] for _ in range(self.k)]
        self.predict(self)
        operation_end_time = time.time() - operation_start_time
        return self.segmented_image, operation_end_time

    def setup_point_array(self):
        image_point_array = []
        for r in range(self.row_count):
            for c in range(self.col_count):
                v = self.segmented_image[r][c]
                p = point(v, r, c)
                image_point_array.append(p)
        return image_point_array

    def find_unique_random_values(self):
        # initialize our centroids
        random_sample_values = None
        unique = False
        while not unique:
            random_sample_values = np.random.choice(self.image_points_array, self.k, replace=False)
            if len(random_sample_values) == len(set(random_sample_values)):
                unique = True
        return random_sample_values

    def predict(self):
        random_sample_values = self.find_unique_random_values(self)
        for cp in random_sample_values:
            self.centroids.append(cp)
        print("assigned random centroids")
        for i in range(self.max_iterations):
            # update clusters
            self.clusters = self.create_clusters(self, self.centroids)
            print("points assigned to clusters")
            # update centroid
            centroids_old = self.centroids
            print("updating centroids to mean")
            self.centroids = get_mean_centroids(self.clusters)
            print("updated centroids to mean")
            # check if converged
            print("checking if converged")
            if self.is_converged(self, centroids_old, self.centroids):
                print("successful convergence at attempt: " + str(i))
                break
            print("attempt: " + str(i + 1) + " of " + str(self.max_iterations))
        # apply diff levels of greyscale to each clustering group
        return self.apply_cluster_group_effects(self, self.clusters)

    def create_clusters(self, centroids):
        clusters = [[] for _ in range(self.k)]
        for p in self.image_points_array:
            closest_centroid_id = closest_centroid(p, centroids)
            if closest_centroid_id > 1:
                print("not 0 or 1")
            clusters[closest_centroid_id].append(p)
        return clusters

    def is_converged(self, centroids_old, centroids):
        distances = []
        for i in range(self.k):
            old_centroid = centroids_old[i]
            mean_centroid = centroids[i]
            dist = euclidean_distance(old_centroid, mean_centroid)
            distances.append(dist)
        # no more chnge so its converged
        return sum(distances) <= self.acceptance_value

    def apply_cluster_group_effects(self, clusters):
        print("assigning values")
        n = 255
        incr = n / self.k
        for cluster in clusters:
            n = n - incr
            for p in cluster:
                self.segmented_image[p.x][p.y] = n
