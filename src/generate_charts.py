import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("results/figures", exist_ok=True)

# Configuration visuelle
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

models = ["Qwen 3.8 (27B)", "GPT-OSS (120B)", "ALLaM (7B)"]
x = np.arange(len(models))
width = 0.25

# --- Graphique 1 : Raisonnement NLI (Test, N=18) ---
nli_ar = [88.9, 100.0, 66.7]
nli_lat = [77.8, 94.4, 38.9]
nli_joint = [72.2, 94.4, 33.3]

rects1 = ax1.bar(x - width, nli_ar, width, label='Arabe (ar)', color='#1f77b4')
rects2 = ax1.bar(x, nli_lat, width, label='Arabizi (lat)', color='#aec7e8')
rects3 = ax1.bar(x + width, nli_joint, width, label='Robuste conjointe (ar ET lat)', color='#2ca02c')

ax1.set_title('Inférence Textuelle (NLI) - Split Test (N=18)', fontsize=13, fontweight='bold', pad=15)
ax1.set_ylabel('Précision / Robustesse (%)', fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(models, fontsize=11, fontweight='bold')
ax1.set_ylim(0, 115)
ax1.axhline(33.3, color='gray', linestyle='--', linewidth=1, label='Hasard (33.3%)')
ax1.legend(loc='upper right', frameon=True)

for rects in [rects1, rects2, rects3]:
    for rect in rects:
        h = rect.get_height()
        ax1.annotate(f'{h:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

# --- Graphique 2 : Qualité de la Conversion (CER) ---
cer_ar_lat = [18.9, 15.2, 89.6]   # ar -> lat
cer_lat_ar = [18.0, 10.1, 31.6]   # lat -> ar

rects4 = ax2.bar(x - width/2, cer_ar_lat, width, label='Arabe → Arabizi (CER %)', color='#d62728')
rects5 = ax2.bar(x + width/2, cer_lat_ar, width, label='Arabizi → Arabe (CER %)', color='#ff7f0e')

ax2.set_title('Taux d’Erreur Caractère (CER) - Conversion (N=14)', fontsize=13, fontweight='bold', pad=15)
ax2.set_ylabel('CER (%) [Plus bas = Meilleur]', fontsize=11)
ax2.set_xticks(x)
ax2.set_xticklabels(models, fontsize=11, fontweight='bold')
ax2.set_ylim(0, 105)
ax2.legend(loc='upper left', frameon=True)

for rects in [rects4, rects5]:
    for rect in rects:
        h = rect.get_height()
        ax2.annotate(f'{h:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
out_path = "results/figures/synthese_3_modeles.png"
plt.savefig(out_path)
print(f"✅ Graphique final haute définition sauvegardé dans : {out_path}")