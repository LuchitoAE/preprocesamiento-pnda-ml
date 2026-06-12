# =============================================================================
# PRACTICA DE CLUSTERING - WINE DATASET
# Algoritmos: K-Means, AGNES (Agglomerative Clustering)
# Visualizacion: PCA, Dendrograma
# Validacion: Metodo del Codo, Coeficiente de Silueta
# =============================================================================

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, confusion_matrix
from scipy.cluster.hierarchy import dendrogram, linkage
import os

os.makedirs("graficos", exist_ok=True)

# =============================================================================
# 1. CARGA Y EXPLORACION DEL DATASET
# =============================================================================
wine = load_wine()
X, y_real = wine.data, wine.target

print("=" * 60)
print(" DATASET WINE")
print("=" * 60)
print(f"  Muestras:        {X.shape[0]}")
print(f"  Caracteristicas:  {X.shape[1]}")
print(f"  Clases reales:    {len(np.unique(y_real))} ({wine.target_names})")
print(f"  Features:         {wine.feature_names}")
print()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(f"  Varianza explicada PCA: {pca.explained_variance_ratio_}")
print(f"  Varianza total 2D:      {pca.explained_variance_ratio_.sum()*100:.1f}%")
print()

# Grafico: Distribucion real
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y_real, cmap='viridis', s=60, alpha=0.8)
ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
ax.set_title('Dataset Wine - Distribucion Real (PCA 2D)')
legend = ax.legend(*scatter.legend_elements(), title="Clase Real")
for i, name in enumerate(wine.target_names):
    legend.get_texts()[i].set_text(f'{i}: {name}')
plt.tight_layout()
plt.savefig('graficos/01_distribucion_real.png', dpi=100, bbox_inches='tight')
plt.close()

# =============================================================================
# 2. METODO DEL CODO (ELBOW)
# =============================================================================
print("=" * 60)
print(" 2. METODO DEL CODO (WCSS / Inercia)")
print("=" * 60)

inercias = []
K_range = range(1, 11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init='auto')
    km.fit(X_scaled)
    inercias.append(km.inertia_)
    print(f"  K={k:2d}  ->  Inercia = {km.inertia_:.2f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(K_range, inercias, 'bo-', markersize=8, linewidth=2)
ax.set_xlabel('Numero de clusters (K)')
ax.set_ylabel('Inercia (WCSS)')
ax.set_title('Metodo del Codo - Dataset Wine')
ax.set_xticks(K_range)
ax.grid(True, alpha=0.3)
ax.annotate('K=3 (Codo)', xy=(3, inercias[2]), xytext=(4.5, inercias[2]*1.3),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=11, color='red', fontweight='bold')
plt.tight_layout()
plt.savefig('graficos/02_metodo_codo.png', dpi=100, bbox_inches='tight')
plt.close()

# =============================================================================
# 3. COEFICIENTE DE SILUETA
# =============================================================================
print("\n" + "=" * 60)
print(" 3. COEFICIENTE DE SILUETA")
print("=" * 60)

sil_scores = []
K_range_sil = range(2, 11)
for k in K_range_sil:
    km = KMeans(n_clusters=k, random_state=42, n_init='auto')
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    sil_scores.append(score)
    print(f"  K={k:2d}  ->  Silhouette = {score:.4f}")

best_k = list(K_range_sil)[np.argmax(sil_scores)]
print(f"\n  K optimo segun Silueta: {best_k}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(K_range_sil, sil_scores, 'go-', markersize=8, linewidth=2)
ax.set_xlabel('Numero de clusters (K)')
ax.set_ylabel('Coeficiente de Silueta')
ax.set_title(f'Metodo de Silueta - K optimo = {best_k}')
ax.set_xticks(K_range_sil)
ax.grid(True, alpha=0.3)
best_score = max(sil_scores)
ax.annotate(f'K={best_k}', xy=(best_k, best_score),
            xytext=(best_k+1, best_score*0.95),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=11, color='red', fontweight='bold')
plt.tight_layout()
plt.savefig('graficos/03_silueta.png', dpi=100, bbox_inches='tight')
plt.close()

# =============================================================================
# 4. K-MEANS (K=3)
# =============================================================================
print("\n" + "=" * 60)
print(" 4. K-MEANS (K=3)")
print("=" * 60)

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
labels_kmeans = kmeans.fit_predict(X_scaled)
centroids_pca = pca.transform(kmeans.cluster_centers_)

print(f"  Inercia:        {kmeans.inertia_:.2f}")
print(f"  Iteraciones:    {kmeans.n_iter_}")
print(f"  Clusters:       {np.bincount(labels_kmeans)}")

cm = confusion_matrix(y_real, labels_kmeans)
print(f"\n  Matriz de confusion (Real vs K-Means):")
print(f"  {cm}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=y_real, cmap='viridis', s=60, alpha=0.8)
axes[0].set_title('Etiquetas Reales')
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_kmeans, cmap='viridis', s=60, alpha=0.8)
axes[1].scatter(centroids_pca[:, 0], centroids_pca[:, 1],
                c='red', s=250, marker='X', edgecolors='black', linewidth=2, label='Centroides')
axes[1].set_title(f'K-Means (K=3)')
axes[1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
axes[1].legend()
plt.tight_layout()
plt.savefig('graficos/04_kmeans.png', dpi=100, bbox_inches='tight')
plt.close()

# =============================================================================
# 5. AGNES - CLUSTERING JERARQUICO
# =============================================================================
print("\n" + "=" * 60)
print(" 5. AGNES - CLUSTERING JERARQUICO (WARD)")
print("=" * 60)

agg = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels_agg = agg.fit_predict(X_scaled)

print(f"  Clusters: {np.bincount(labels_agg)}")

cm_agg = confusion_matrix(y_real, labels_agg)
print(f"\n  Matriz de confusion (Real vs AGNES):")
print(f"  {cm_agg}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=y_real, cmap='viridis', s=60, alpha=0.8)
axes[0].set_title('Etiquetas Reales')
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_agg, cmap='viridis', s=60, alpha=0.8)
axes[1].set_title('AGNES - Clustering Jerarquico (K=3, Ward)')
axes[1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
plt.tight_layout()
plt.savefig('graficos/05_agnes.png', dpi=100, bbox_inches='tight')
plt.close()

# =============================================================================
# 6. DENDROGRAMA
# =============================================================================
print("\n" + "=" * 60)
print(" 6. DENDROGRAMA (AGNES - Ward)")
print("=" * 60)

linked = linkage(X_scaled, method='ward')

fig, ax = plt.subplots(figsize=(16, 7))
dendrogram(linked, leaf_rotation=90, leaf_font_size=8, color_threshold=0)
ax.set_title('Dendrograma - Clustering Jerarquico (Ward) - Dataset Wine')
ax.set_xlabel('Indice de muestra')
ax.set_ylabel('Distancia (Ward)')

cut_height = linked[-(3-1), 2]
ax.axhline(y=cut_height, color='red', linestyle='--', linewidth=2,
           label=f'Corte K=3 (altura ~ {cut_height:.1f})')
ax.legend()
plt.tight_layout()
plt.savefig('graficos/06_dendrograma.png', dpi=100, bbox_inches='tight')
plt.close()

# =============================================================================
# 7. COMPARACION FINAL
# =============================================================================
print("\n" + "=" * 60)
print(" 7. COMPARACION FINAL")
print("=" * 60)

sil_kmeans = silhouette_score(X_scaled, labels_kmeans)
sil_agg = silhouette_score(X_scaled, labels_agg)

print(f"  Silhouette K-Means:  {sil_kmeans:.4f}")
print(f"  Silhouette AGNES:    {sil_agg:.4f}")

pureza_km = np.sum(np.max(cm, axis=0)) / len(y_real)
pureza_agg = np.sum(np.max(cm_agg, axis=0)) / len(y_real)
print(f"\n  Pureza K-Means: {pureza_km*100:.1f}%")
print(f"  Pureza AGNES:   {pureza_agg*100:.1f}%")

# Grafico comparativo final
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
titles = ['Etiquetas Reales', 'K-Means (K=3)', 'AGNES - Ward (K=3)']
labels_list = [y_real, labels_kmeans, labels_agg]

for ax, lab, title in zip(axes, labels_list, titles):
    ax.scatter(X_pca[:, 0], X_pca[:, 1], c=lab, cmap='viridis', s=60, alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')

plt.tight_layout()
plt.savefig('graficos/07_comparacion_final.png', dpi=100, bbox_inches='tight')
plt.close()

# =============================================================================
# RESUMEN
# =============================================================================
print("\n" + "=" * 60)
print(" RESUMEN FINAL")
print("=" * 60)
print(f"  Dataset:            Wine ({X.shape[0]} muestras, {X.shape[1]} features, 3 clases)")
print(f"  K optimo (Codo):    3")
print(f"  K optimo (Silueta): {best_k}")
print(f"  Silhouette K-Means: {sil_kmeans:.4f}")
print(f"  Silhouette AGNES:   {sil_agg:.4f}")
print(f"  Pureza K-Means:     {pureza_km*100:.1f}%")
print(f"  Pureza AGNES:       {pureza_agg*100:.1f}%")
print(f"\n  Graficos guardados en: graficos/")
print("=" * 60)
