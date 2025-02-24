from typing import Optional, Dict, Literal, List
from enum import Enum
import json

from . import _constants as constants
from ._api import OpenAPI


class BaseAnalysis(OpenAPI):
    def _extract_id(self, data_id: str, table_id: Optional[str] = None):
        data_details = self.get_sample_data_detail(data_id)
        study_id = data_details[constants.ConnectorKeys.STUDY_ID.value]
        sample_id = data_details[constants.ConnectorKeys.SAMPLE_ID.value]
        if table_id is None:
            table_results = []
            submitted_results: Dict[str, Dict[str, dict]] = \
                data_details[constants.ConnectorKeys.MAP_SUBMIT_RESULT.value]
            for _, res in submitted_results.items():
                table_results.extend(
                    res.get(constants.ConnectorKeys.ANNOTATED_DATA.value, {}).keys())
            if len(table_results) == 0:
                raise RuntimeError("Not found any annotated data.")
            if len(table_results) > 1:
                raise RuntimeError(
                    f"Found too many annotated data: {table_results}. "
                    "Please identify an ID by `table_id=...`"
                )
            table_id = table_results[0]
        return study_id, sample_id, table_id

    def _post_analysis(
        self,
        data_id: str,
        title: str,
        params: dict,
        sub_type: str,
        group_type: str,
        table_id: Optional[str] = None,
        **_,
    ):
        study_id, sample_id, table_id = self._extract_id(data_id, table_id=table_id)
        return self.post_openapi_request(
            url=constants.CREATE_ANALYSIS_URL,
            json={
                constants.ConnectorKeys.DATA.value: {
                    constants.ConnectorKeys.TITLE.value: title,
                    constants.ConnectorKeys.PARAMS.value: json.dumps(params),
                    constants.ConnectorKeys.DISPLAY_PARAMS.value: json.dumps({}),
                    constants.ConnectorKeys.SUB_TYPE.value: sub_type,
                    constants.ConnectorKeys.GROUP_TYPE.value: group_type,
                    constants.ConnectorKeys.DESCRIPTION.value: title,
                },
                constants.ConnectorKeys.STUDY_ID.value: study_id,
                constants.ConnectorKeys.SAMPLE_ID.value: sample_id,
                constants.ConnectorKeys.DATA_ID.value: data_id,
                constants.ConnectorKeys.TABLE_ID.value: table_id,
            }
        )


class Embeddings(BaseAnalysis):
    def pca(
        self,
        data_id: str,
        normalize_method: Optional[
            Literal[
                constants.NormalizeMethod.RAW,
                constants.NormalizeMethod.LOG1P_NORMALIZE,
                constants.NormalizeMethod.SQRT_NORMALIZE,
            ]
        ] = constants.NormalizeMethod.LOG1P_NORMALIZE,
        title: Optional[str] = None,
        batch_key: Optional[str] = None,
        n_top_genes: Optional[int] = None,
        **kwargs,
    ):
        """
        Principal Component Analysis

        Parameters
        ----------
        data_id: `str`
            ID of a data in sample.
        normalize_method: `Literal["raw", "log1p-normalized", "sqrt-normalized"]`, Default: "log1p-normalized"
            Using raw expression or scaling (log1p, square root) to normalize when running PCA.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        batch_key: `Optional[str]`, Default: None
            Metadata which defines batch effect.
            If provided, using Harmony to remove batch effect.
        n_top_genes: `Optional[int]`, Default: None
            Number of top highly variable genes.
            If provided, running highly variable genes to select genes for PCA.
        """
        if isinstance(normalize_method, Enum):
            normalize_method = normalize_method.value

        return self._post_analysis(
            data_id=data_id,
            title=title if title is not None else "PCA",
            params={
                "normalize_method": normalize_method,
                "name": title,
                "batch_key": batch_key,
                "n_top_genes": n_top_genes,
                **kwargs,
            },
            sub_type="PCA",
            group_type="embedding",
            **kwargs,
        )

    def scvi(
        self,
        data_id: str,
        n_latents: int = 20,
        title: Optional[str] = None,
        batch_key: Optional[str] = None,
        n_top_genes: Optional[int] = 2000,
        **kwargs,
    ):
        """
        Reducing dimensions with scVI

        Parameters
        ----------
        data_id: `str`
            ID of a data in sample.
        n_latents: `int`, Default: 20
            Number of latents.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        batch_key: `Optional[str]`, Default: None
            Metadata which defines batch effect.
            If provided, using Harmony to remove batch effect.
        n_top_genes: `Optional[int]`, Default: 2000
            Number of top highly variable genes.
            If provided, running highly variable genes to select genes for PCA.
        """
        return self._post_analysis(
            data_id=data_id,
            title=title if title is not None else "scVI",
            params={
                "n_latents": n_latents,
                "name": title,
                "batch_key": batch_key,
                "n_top_genes": n_top_genes,
                **kwargs,
            },
            sub_type="scVI",
            group_type="embedding",
            **kwargs,
        )

    def umap(
        self,
        data_id: str,
        embedding_key: str,
        n_neighbors: int = 15,
        local_connectivity: float = 1,
        init: Literal["pca", "spectral", "random"] = "pca",
        deterministic: bool = True,
        title: Optional[str] = None,
        **kwargs,
    ):
        """
        Uniform Manifold Approximation and Projection for Dimension Reduction.

        Parameters
        ----------
        data_id: `str`
            ID of a data in sample.
        embedding_key: `str`
            Embedding to run UMAP, should be result of PCA or scVI.
        n_neighbors : Optional[`int`], Default: None
            The number of nearest neighbors.
        local_connectivity : `float`, Default: 1.0
            The local connectivity required -- i.e. the number of nearest
            neighbors that should be assumed to be connected at a local level.
            The higher this value the more connected the manifold becomes
            locally. In practice this should be not more than the local intrinsic
            dimension of the manifold.
        init : `str`, Default: "pca"
            How to initialize the low dimensional embedding. Options are:
            * `"spectral"` : use a spectral embedding of the fuzzy 1-skeleton (non-deterministic).
            * `"random"` : assign initial embedding positions at random.
            * `"pca"` : pca low dimensions of input matrix.
        deterministic : `bool`, Default: True
            Making sure with same initialization, results will remains the same across runs on the same device.
            Deterministic version will converge a lot slower on big datasets (hence lower quality on same setting).
            If you prefer quality/performance, disable `deterministic`
            Note: `"spectral"` initialization is non-deterministic across runs.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        """
        return self._post_analysis(
            data_id=data_id,
            title=title if title is not None else "UMAP",
            params={
                "embedding_key": embedding_key,
                "n_neighbors": n_neighbors,
                "local_connectivity": local_connectivity,
                "init": init,
                "deterministic": deterministic,
                "name": title,
                **kwargs,
            },
            sub_type="UMAP",
            group_type="embedding",
            **kwargs,
        )

    def tsne(
        self,
        data_id: str,
        embedding_key: str,
        n_neighbors: int = 90,
        perplexity: float = 30,
        local_connectivity: float = 1,
        init: Literal["pca", "gaussian", "input"] = "pca",
        title: Optional[str] = None,
        **kwargs,
    ):
        """
        FFT-accelerated Interpolation-based t-SNE implementation.

        Parameters
        ----------
        data_id: `str`
            ID of a data in sample.
        embedding_key: `str`
            Embedding to run UMAP, should be result of PCA or scVI.
        n_neighbors : Optional[`int`], Default: None
            The number of nearest neighbors.
        perplexity : ``float``, default = ``30``
            The perplexity is related to the number of nearest neighbors that is used in
            other manifold learning algorithms.
            Larger datasets usually require a larger perplexity.
            Consider selecting a value between ``5`` and ``50``.
            Different values can result in significantly different results.
        local_connectivity : `float`, Default: 1.0
            The local connectivity required -- i.e. the number of nearest
            neighbors that should be assumed to be connected at a local level.
            The higher this value the more connected the manifold becomes
            locally. In practice this should be not more than the local intrinsic
            dimension of the manifold.
        init : `str`, Default: "pca"
            How to initialize the low dimensional embedding. Options are:
            * ``"gaussian"`` : init using gaussian noise.
            * ``"input"`` : 2 first row input matrix.
            * ``"pca"`` : pca 2 first row input matrix.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        """
        return self._post_analysis(
            data_id=data_id,
            title=title if title is not None else "t-SNE",
            params={
                "embedding_key": embedding_key,
                "n_neighbors": n_neighbors,
                "local_connectivity": local_connectivity,
                "init": init,
                "perplexity": perplexity,
                "name": title,
                **kwargs,
            },
            sub_type="t-SNE",
            group_type="embedding",
            **kwargs,
        )


class Clustering(BaseAnalysis):
    def louvain(
        self,
        data_id: str,
        embedding_key: str,
        resolution: float,
        n_neighbors: int = 90,
        local_connectivity: float = 1,
        title: Optional[str] = None,
        **kwargs,
    ):
        """
        Louvain clustering implementation.

        Parameters
        ----------
        data_id: `str`
            ID of a data in sample.
        embedding_key: `str`
            Embedding to run UMAP, should be result of PCA or scVI.
        resolution : ``float``
            Resolution parameter, higher lead to more communities.
        n_neighbors : Optional[`int`], Default: None
            The number of nearest neighbors.
        local_connectivity : `float`, Default: 1.0
            The local connectivity required -- i.e. the number of nearest
            neighbors that should be assumed to be connected at a local level.
            The higher this value the more connected the manifold becomes
            locally. In practice this should be not more than the local intrinsic
            dimension of the manifold.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        """
        return self._post_analysis(
            data_id=data_id,
            title=title if title is not None else "Louvain",
            params={
                "embedding_key": embedding_key,
                "resolution": resolution,
                "n_neighbors": n_neighbors,
                "local_connectivity": local_connectivity,
                "name": title,
                **kwargs,
            },
            sub_type="Louvain",
            group_type="clustering",
            **kwargs,
        )

    def kmeans(
        self,
        data_id: str,
        embedding_key: str,
        n_clusters: int,
        title: Optional[str] = None,
        **kwargs,
    ):
        """
        k-means clustering implementation.

        Parameters
        ----------
        data_id: `str`
            ID of a data in sample.
        embedding_key: `str`
            Embedding to run UMAP, should be result of PCA or scVI.
        n_clusters: ``int``
            Number of clusters.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        """
        return self._post_analysis(
            data_id=data_id,
            title=title if title is not None else "k-means",
            params={
                "embedding_key": embedding_key,
                "n_clusters": n_clusters,
                "name": title,
                **kwargs,
            },
            sub_type="k-means",
            group_type="clustering",
            **kwargs,
        )


class DE(BaseAnalysis):
    def differential_expression_genes(
        self,
        data_id_1: str,
        data_id_2: str,
        group_1_indices: List[int],
        group_2_indices: List[int],
        group_1_name: str = "Group 1",
        group_2_name: str = "Group 2",
        method: Literal["venice", "t-test", "wilcoxon"] = "venice",
        normalize_method: Optional[
            Literal[
                constants.NormalizeMethod.RAW,
                constants.NormalizeMethod.LOG1P_NORMALIZE,
                constants.NormalizeMethod.SQRT_NORMALIZE,
            ]
        ] = constants.NormalizeMethod.LOG1P_NORMALIZE,
        title: Optional[str] = None,
        **kwargs,
    ):
        """
        Spatial Region Segmentation.

        Parameters
        ----------
        data_id_1: `str`
            ID of the first data to run differential expression genes.
        data_id_2: `str`
            ID of the second data to run differential expression genes.
        group_1_indices: `List[int]`
            Cell indices to compare in the first group.
        group_2_indices: `List[int]`
            Cell indices to compare in the second group.
        group_1_name: `str`, Default: "Group 1"
            Name of the first group.
        group_2_name: `str`, Default: "Group 2"
            Name of the second group.
        method: `Literal["venice", "t-test", "wilcoxon"]`, Default: "venice"
            Test statistic method.
        normalize_method: `Literal["raw", "log1p-normalized", "sqrt-normalized"]`, Default: "log1p-normalized"
            Using raw expression or scaling (log1p, square root) for test statistic.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        """
        _, sample_id_1, table_id_1 = self._extract_id(data_id_1)
        _, sample_id_2, table_id_2 = self._extract_id(data_id_2)
        if isinstance(normalize_method, Enum):
            normalize_method = normalize_method.value

        return self._post_analysis(
            data_id=data_id_1,
            title=title if title is not None else "DE genes",
            params={
                "group_1_indices": group_1_indices,
                "group_2_indices": group_2_indices,
                "group_1_name": group_1_name,
                "group_2_name": group_2_name,
                "method": method,
                "normalize_method": normalize_method,
                "sample_id_1": sample_id_1,
                "sample_id_2": sample_id_2,
                "table_id_1": table_id_1,
                "table_id_2": table_id_2,
                "name": title,
                **kwargs,
            },
            sub_type="de_genes",
            group_type="deg",
            **kwargs,
        )


class Prediction(BaseAnalysis):
    def metadata_reference(
        self,
        data_id: str,
        cluster_key: str,
        species: str,
        anno_type: Literal["sub", "major"] = "sub",
        title: Optional[str] = None,
        **kwargs,
    ):
        """
        Spatial Region Segmentation.

        Parameters
        ----------
        data_id: `str`
            ID of a data in sample.
        cluster_key: `str`
            Cluster to predict cell types.
        species: `str`
            Species of data.
        anno_type: `Literal["sub", "major"]`, Default: "sub"
            Type of annotation: Major or sub cell types.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        """
        return self._post_analysis(
            data_id=data_id,
            title=title if title is not None else "Metadata Reference",
            params={
                "cluster_key": cluster_key,
                "anno_type": anno_type,
                "species": species,
                "name": title,
                **kwargs,
            },
            sub_type="celltype_prediction",
            group_type="prediction",
            **kwargs,
        )


class SpatialAnalysis(BaseAnalysis):
    def region_segmentation(
        self,
        data_id: str,
        radius: float,
        mpp: float,
        species: str,
        resolution: float = 0.5,
        title: Optional[str] = None,
        **kwargs,
    ):
        """
        Spatial Region Segmentation.

        Parameters
        ----------
        data_id: `str`
            ID of a data in sample.
        radius: `float`
            Radius (micrometer) to build spatial graph
        mpp: `float`
            Micrometers per pixel.
        species: `str`
            Species of data.
        resolution : ``float``, Default: 0.5
            Resolution parameter, higher lead to more communities.
        title: `Optional[str]`, Default: None
            Title of analysis, it will be used as name of embeddings.
            If not provided, a default name will be used.
        """
        data_details = self.get_sample_data_detail(data_id)
        transcripts = []
        spots = []
        submitted_results: Dict[str, Dict[str, dict]] = \
            data_details[constants.ConnectorKeys.MAP_SUBMIT_RESULT.value]
        for _, res in submitted_results.items():
            transcripts.extend(res.get(constants.ConnectorKeys.TRANSCRIPTS.value, {}).keys())
            spots.extend(res.get(constants.ConnectorKeys.SPOT.value, {}).keys())
        transcripts_id = transcripts[0] if len(transcripts) > 0 else None
        spots_id = spots[0] if len(spots) > 0 else None

        return self._post_analysis(
            data_id=data_id,
            title=title if title is not None else "Region Segmentation",
            params={
                "radius": radius,
                "mpp": mpp,
                "resolution": resolution,
                "species": species,
                "transcripts_id": transcripts_id,
                "spots_id": spots_id,
                "name": title,
                **kwargs,
            },
            sub_type="segmentation_by_spatial_correlation",
            group_type="svg",
            **kwargs,
        )


class Analysis(BaseAnalysis):
    def __init__(
        self,
        domain: str,
        token: str,
        verify_ssl: bool = False,
    ):
        super().__init__(domain, token, verify_ssl=verify_ssl)
        self.embeddings = Embeddings(domain, token, verify_ssl=verify_ssl)
        self.clustering = Clustering(domain, token, verify_ssl=verify_ssl)
        self.de = DE(domain, token, verify_ssl=verify_ssl)
        self.prediction = Prediction(domain, token, verify_ssl=verify_ssl)
        self.spatial_analysis = SpatialAnalysis(domain, token, verify_ssl=verify_ssl)

    def list_metadata(self, data_id: str):
        study_id, sample_id, table_id = self._extract_id(data_id)
        return self.post_pyapi_request(
            url=constants.GET_ANNOTATED_ELEMENTS,
            json={
                constants.ConnectorKeys.STUDY_ID.value: study_id,
                constants.ConnectorKeys.SAMPLE_ID.value: sample_id,
                constants.ConnectorKeys.TABLE_ID.value: table_id,
                constants.ConnectorKeys.ELEMENT.value: constants.ConnectorKeys.OBS.value,
            },
        )

    def list_embedding(self, data_id: str):
        study_id, sample_id, table_id = self._extract_id(data_id)
        return self.post_pyapi_request(
            url=constants.GET_ANNOTATED_ELEMENTS,
            json={
                constants.ConnectorKeys.STUDY_ID.value: study_id,
                constants.ConnectorKeys.SAMPLE_ID.value: sample_id,
                constants.ConnectorKeys.TABLE_ID.value: table_id,
                constants.ConnectorKeys.ELEMENT.value: constants.ConnectorKeys.OBSM.value,
            },
        )
