import numpy as np
from numpy.typing import NDArray
from sklearn.cluster import KMeans


class AggregateBalancingKmeans:
    def __init__(
        self, k: int, *, initial_centroids: NDArray = None, tolerance: int = 9
    ) -> None:
        self.k = k
        self.tolerance = tolerance
        self.Y_features = None
        self.X_features = None
        self.weights = None
        self.m = None
        self.N = None
        self.centroids = initial_centroids
        self.labels: NDArray = None
        self.membership: NDArray = None
        self.Ti: NDArray = None
        self.Tij: NDArray = None
        self.rng = np.random.default_rng()

    def _generate_membership(self):
        membership = np.zeros((self.N, self.k))
        for j in range(self.N):
            membership[j, self.labels[j]] = 1
        return membership

    def _generate_Tij(self) -> NDArray:
        return np.sum(self.X_features[:, :, np.newaxis] * self.membership[:, np.newaxis, :], axis=0)

    def _generate_Ti(self) -> NDArray:
        return np.linalg.norm(self._generate_Tij()*(self.weights[:, np.newaxis]**(1/2)), axis=0)

    def _generate_total_Ti(self) -> NDArray:
        return np.sum(self._generate_Tij()*(self.weights[:, np.newaxis]**(1/2)), axis=0)

    def _transfer_score(
        self,
        y_vec: NDArray,
        current_cluster_indx: float,
        new_cluster_indx: float,
    ) -> float:
        total_Ti = self._generate_total_Ti()
        if (
            (
            #     self.Ti[current_cluster_indx]
            #     - self.Ti[new_cluster_indx]
            #     > 10**-self.tolerance
            # ) and (
                total_Ti[current_cluster_indx]
                - total_Ti[new_cluster_indx]
                > 10**-self.tolerance
            )
        ):
            return (
                np.linalg.norm(y_vec - self.centroids[new_cluster_indx]) ** 2
                - np.linalg.norm(y_vec - self.centroids[current_cluster_indx]) ** 2
            ) / np.linalg.norm(
                total_Ti[current_cluster_indx]
                - total_Ti[new_cluster_indx]
                + 1e-9
            )**2
        else:
            return np.inf

    def _get_transfer_records(self, top_m: int):
        costs = []

        for i in range(self.N):
            for j_old in np.nonzero(self.membership[i])[0]:
                j_new_min = np.argmin(
                    [self._transfer_score(self.Y_features[i], j_old, j_new) for j_new in range(self.k)]
                )
                cost = self._transfer_score(self.Y_features[i], j_old, j_new_min)
                costs.append((cost, i, j_old, j_new_min))

        costs = np.array(costs)

        print()
        print('cost')
        print(costs[np.argsort(costs[:, 0])][:10])
        print()

        return costs[np.argsort(costs[:, 0])][:top_m, 1:].astype(int)

    def _transfer(self, data_index: int, from_index: int, to_index: int) -> None:
        total_Ti = self._generate_total_Ti()
        # print("total_Ti", total_Ti)
        # print("total_Ti[from_index]", total_Ti[from_index], "total_Ti[to_index]", total_Ti[to_index])

        # print(self.Tij.shape)

        # transfer = min(
        #     np.min(self.membership[data_index, from_index] * np.abs(self.X_features[data_index])),
        #     np.sum(self.weights*(self.Tij[:, from_index]**2 - self.Tij[:, to_index]**2))/np.sum(2*self.weights*(self.Tij[:, from_index] + self.Tij[:, to_index]))
        # )

        # percent = np.sum(self.weights*(self.Tij[:, from_index]**2 - self.Tij[:, to_index]**2))/np.sum(2*self.X_features[data_index]*self.weights*(self.Tij[:, from_index] + self.Tij[:, to_index]))

        # print("percent", percent)
        # print(np.sum(self.weights*(self.Tij[:, from_index]**2 - self.Tij[:, to_index]**2)), np.sum(2*self.X_features[data_index]*self.weights*(self.Tij[:, from_index] + self.Tij[:, to_index])))

        # print("BEFORE", self.Tij[:, from_index], self.Tij[:, to_index])

        # print("transfer_prob", transfer)
        # print(self.membership[data_index, from_index] * np.abs(self.X_features[data_index]))

        print('BEFORE', self.membership[data_index])

        percent = self.membership[data_index, from_index]/4
        # transfer = percent * self.X_features[data_index]

        self.membership[data_index, from_index] -= percent
        self.membership[data_index, to_index] += percent

        print('AFTER', self.membership[data_index])

        # self.membership[data_index, from_index] = (
        #     np.sum(self.membership[data_index, from_index] * self.X_features[data_index] - transfer)/np.sum(self.X_features[data_index])
        # )
        # self.membership[data_index, to_index] = (
        #     np.sum(self.membership[data_index, to_index] * self.X_features[data_index] + transfer)/np.sum(self.X_features[data_index])
        # )

    def _no_transfer_possible(self, transfer_records: NDArray) -> bool:
        return transfer_records[0, 0] == np.inf

    def _is_transfer_possible(self, from_cluster: int, to_cluster: int) -> bool:
        return (
            self.Ti[from_cluster] - self.Ti[to_cluster]
            > 10**-self.tolerance
        )

    def _stop_codition(self, tol) -> bool:
        return np.all(np.abs(self.Ti) < 10**-tol)

    def _expected_num_transfers(self) -> float:
        max_diff_sum = np.max(self.Ti - self.Ti[:, None])
        mean_nonzero_probs = np.mean(
            self.membership[np.nonzero(self.membership)]
        )
        return max(int(np.floor(max_diff_sum / (2 * mean_nonzero_probs))), 1)

    def _update_centroids(self) -> None:
        self.centroids = np.mean(self.Y_features[:, :, np.newaxis] * self.membership[:, np.newaxis, :], axis=0).T

    def fit(self, Y_features: NDArray, X_features: NDArray, weights: NDArray) -> None:
        self.Y_features = Y_features
        self.X_features = X_features
        self.weights = weights
        self.m = X_features.shape[1]
        self.N = X_features.shape[0]

        kmeans = KMeans(
            n_clusters=self.k,
            init=self.centroids if self.centroids is not None else "k-means++",
            n_init=10,
            tol=10**-self.tolerance,
        )
        kmeans.fit(self.Y_features)

        self.centroids = kmeans.cluster_centers_
        self.labels = kmeans.labels_
        self.membership = self._generate_membership()
        self.Tij = self._generate_Tij()
        print("Tij", self.Tij.shape)

        self.Ti = self._generate_Ti()

        print("Ti", self.Ti.shape)

        print("centroids", self.centroids)

        iter_ = 0

        while not self._stop_codition(self.tolerance) and iter_ < 100:
            print()
            print("iter:", iter_)
            # print("Tij", self.Tij)
            print("norm Ti", self.Ti)
            print("Ti", self._generate_total_Ti())
            print()
            transfer_records = self._get_transfer_records(top_m=self._expected_num_transfers())
            if self._no_transfer_possible(transfer_records):
                break
            for data_index, from_cluster_index, to_cluster_index in transfer_records:
                if self._is_transfer_possible(from_cluster_index, to_cluster_index):
                    self._transfer(data_index, from_cluster_index, to_cluster_index)
                    self.Tij = self._generate_Tij()
                    self.Ti = self._generate_Ti()
                    # print("AFTER", self.Tij[:, from_cluster_index], self.Tij[:, to_cluster_index])
                    print()
            self._update_centroids()
            print("centroids", self.centroids)
            iter_ += 1

    def get_clusters(self) -> NDArray:
        clusters = []

        for i in range(self.k):
            probs = self.membership[:, i]
            ids = np.nonzero(probs)[0]
            units = np.concatenate(
                [ids.reshape(-1, 1), self.Y_features[ids], probs[ids].reshape(-1, 1)], axis=1
            )
            clusters.append(units)

        return clusters
