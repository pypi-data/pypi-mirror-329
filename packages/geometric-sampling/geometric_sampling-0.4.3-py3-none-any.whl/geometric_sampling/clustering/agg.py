import numpy as np
from numpy.typing import NDArray
from sklearn.cluster import KMeans


class Agg:
    def __init__(
        self, k: int, *, initial_centroids: NDArray = None, tolerance: int = 5
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
        return np.sum(
            self.X_features[:, :, np.newaxis] * self.membership[:, np.newaxis, :],
            axis=0,
        ).T

    def _generate_Ti(self) -> NDArray:
        return np.sum((self.weights[np.newaxis, :]) * self._generate_Tij(), axis=1)

    def _weighet_norm(self, array: NDArray) -> NDArray:
        return np.sum(self.weights * array**2)

    def _minimum_percent(self, data_index: int, from_index: int, to_index: int):
        return np.sum(
            self.weights
            * self.X_features[data_index]
            * (self.Tij[from_index] - self.Tij[to_index])
        ) / (2 * np.sum(self.weights * self.X_features[data_index] ** 2))

    def _zero_percent(self, data_index: int, cluster: int):
        return np.sum(
            self.weights * self.X_features[data_index] * self.Tij[cluster]
        ) / (np.sum(self.weights * self.X_features[data_index] ** 2))

    def _transfer_percent(
        self,
        data_index: int,
        old_cluster: int,
        new_cluster: int,
    ):
        if (
            self.Ti[old_cluster] >= - 10**-self.tolerance
            and self.Ti[new_cluster] >= - 10**-self.tolerance
        ) or (
            self.Ti[old_cluster] <= 10**-self.tolerance
            and self.Ti[new_cluster] <= 10**-self.tolerance
        ):
            return min(
                self.membership[data_index, old_cluster],
                self._minimum_percent(data_index, old_cluster, new_cluster)
            )
        else:
            return min(
                self.membership[data_index, old_cluster],
                max(0, self._zero_percent(data_index, old_cluster)),
                max(0, -self._zero_percent(data_index, new_cluster)),
            )

    def _transfer_score(
        self,
        data_index: int,
        old_cluster: int,
        new_cluster: int,
        printing: bool = False,
    ) -> float:
        if printing:
            print()
            print(f'Transfer score: {round((
                np.linalg.norm(self.Y_features[data_index] - self.centroids[new_cluster]) ** 2
                - np.linalg.norm(self.Y_features[data_index] - self.centroids[old_cluster]) ** 2
            ) / self._weighet_norm(
                self.Tij[old_cluster]
                - self.Tij[new_cluster]
                + 1e-9
            ), 2)}')
            print(f'UP: {round(np.linalg.norm(self.Y_features[data_index] - self.centroids[new_cluster]) ** 2, 2)} - {round(np.linalg.norm(self.Y_features[data_index] - self.centroids[old_cluster]) ** 2, 2)} = {round(np.linalg.norm(self.Y_features[data_index] - self.centroids[new_cluster]) ** 2
                - np.linalg.norm(self.Y_features[data_index] - self.centroids[old_cluster]) ** 2, 2)}')
            print(f'DOWN: {round(self._weighet_norm(
                self.Tij[old_cluster]
                - self.Tij[new_cluster]
                + 1e-9
            ), 2)}')
            print()
        if (
            self._transfer_percent(data_index, old_cluster, new_cluster)
            > 10**-self.tolerance
        ):
            return (
<<<<<<< Updated upstream
                np.linalg.norm(
                    self.Y_features[data_indx] - self.centroids[new_cluster_indx]
                )
                ** 2
                - np.linalg.norm(
                    self.Y_features[data_indx] - self.centroids[current_cluster_indx]
                )
                ** 2
            ) / self._weighet_norm(
                self.Tij[current_cluster_indx] - self.Tij[new_cluster_indx] + 1e-9
=======
                np.linalg.norm(self.Y_features[data_index] - self.centroids[new_cluster]) ** 2
                - np.linalg.norm(self.Y_features[data_index] - self.centroids[old_cluster]) ** 2
            ) / self._weighet_norm(
                self.Tij[old_cluster]
                - self.Tij[new_cluster]
                + 1e-9
>>>>>>> Stashed changes
            )
        else:
            return np.inf

    def _get_transfer_records(self, top_m: int):
        costs = []

        for i in range(self.N):
            for j_old in np.nonzero(self.membership[i])[0]:
                j_new_min = np.argmin(
                    [self._transfer_score(i, j_old, j_new) for j_new in range(self.k)]
                )
                cost = self._transfer_score(i, j_old, j_new_min)
                costs.append((cost, i, j_old, j_new_min))

        costs = np.array(costs)

        print()
<<<<<<< Updated upstream
        print("cost")
        print(costs[np.argsort(costs[:, 0])][:10])
=======
        print('cost')
        print(costs[np.argsort(costs[:, 0])][:5])
>>>>>>> Stashed changes
        print()

        return costs[np.argsort(costs[:, 0])][:top_m, 1:].astype(int)

<<<<<<< Updated upstream
    def _transfer(self, data_index: int, from_index: int, to_index: int) -> None:
        if (
            self.Ti[from_index] >= -(10**-self.tolerance)
            and self.Ti[to_index] >= -(10**-self.tolerance)
        ) or (
            self.Ti[from_index] <= 10**-self.tolerance
            and self.Ti[to_index] <= 10**-self.tolerance
        ):
            transfer_percent = min(
                self.membership[data_index, from_index],
                self._minimum_percent(data_index, from_index, to_index),
            )
        else:
            transfer_percent = min(
                self.membership[data_index, from_index],
                max(0, self._zero_percent(data_index, from_index)),
                max(0, -self._zero_percent(data_index, to_index)),
            )
=======
    def _transfer(self, data_index: int, old_cluster: int, new_cluster: int) -> None:
>>>>>>> Stashed changes

        transfer_percent = self._transfer_percent(data_index, old_cluster, new_cluster)

        print(f'Transfer {data_index} from {old_cluster} to {new_cluster}')
        print(f'from cluster: Ti {self.Ti[old_cluster]} - Norm {self._weighet_norm(self.Tij[old_cluster])}')
        print(f'to cluster: Ti {self.Ti[new_cluster]} - Norm {self._weighet_norm(self.Tij[new_cluster])}')
        self._transfer_score(data_index, old_cluster, new_cluster, True)
        print('transfer_percent', transfer_percent)
        print()

        self.membership[data_index, old_cluster] -= transfer_percent
        self.membership[data_index, new_cluster] += transfer_percent

    def _no_transfer_possible(self, transfer_records: NDArray) -> bool:
        return transfer_records[0, 0] == np.inf

    def _is_transfer_possible(self, from_cluster: int, to_cluster: int) -> bool:
        return True
        # return (
        #     np.linalg.norm(self.Ti[from_cluster] - self.Ti[to_cluster])
        #     > 10**-self.tolerance
        # )

    def _stop_codition(self, tol) -> bool:
        return np.all(np.abs(self.Ti) < 10**-tol)

    def _expected_num_transfers(self) -> float:
        max_diff_sum = np.max(self.Ti - self.Ti[:, None])
        mean_nonzero_probs = np.mean(self.membership[np.nonzero(self.membership)])
        return max(int(np.floor(max_diff_sum / (2 * mean_nonzero_probs))), 1)

    def _update_centroids(self) -> None:
<<<<<<< Updated upstream
        self.centroids = np.mean(
            self.Y_features[:, :, np.newaxis] * self.membership[:, np.newaxis, :],
            axis=0,
        ).T
=======
        for i in range(self.k):
            self.centroids[i] = np.mean(self.Y_features[self.membership[:, i] > 0], axis=0)
>>>>>>> Stashed changes

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
        self.Ti = self._generate_Ti()
        iter_ = 0

        while not self._stop_codition(self.tolerance) and iter_ < 1000:
            print('================================================')
            print("iter:", iter_)
            print("Ti", self.Ti)
            print()
            transfer_records = self._get_transfer_records(top_m=1)
            if self._no_transfer_possible(transfer_records):
                break
            for data_index, old_cluster, new_cluster in transfer_records:
                if self._is_transfer_possible(old_cluster, new_cluster):
                    self._transfer(data_index, old_cluster, new_cluster)
                    self.Tij = self._generate_Tij()
                    self.Ti = self._generate_Ti()
            self._update_centroids()
            iter_ += 1
