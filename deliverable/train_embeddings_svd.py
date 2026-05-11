import os
import re
import json
import numpy as np


def limpiar_texto(texto: str):
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ\s]", "", texto)
    return texto.split()


def leer_corpus(path: str):
    with open(path, "r", encoding="utf-8") as f:
        texto = f.read()
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    oraciones = []
    for p in parrafos:
        partes = re.split(r'[.!?]+', p)
        for s in partes:
            s = s.strip()
            if s:
                oraciones.append(limpiar_texto(s))
    return oraciones


def build_cooccurrence(sentences, window=4):
    vocab = {}
    inv_vocab = []
    for sent in sentences:
        for w in sent:
            if w not in vocab:
                vocab[w] = len(inv_vocab)
                inv_vocab.append(w)

    V = len(inv_vocab)
    M = np.zeros((V, V), dtype=np.float64)

    for sent in sentences:
        ids = [vocab[w] for w in sent]
        for i, wi in enumerate(ids):
            start = max(0, i - window)
            end = min(len(ids), i + window + 1)
            for j in range(start, end):
                if i == j:
                    continue
                wj = ids[j]
                M[wi, wj] += 1.0

    return M, vocab, inv_vocab


def compute_svd_embeddings(M, n_components=100):
    U, s, Vt = np.linalg.svd(M, full_matrices=False)
    k = min(n_components, U.shape[1])
    S_sqrt = np.sqrt(s[:k])
    emb = U[:, :k] * S_sqrt[np.newaxis, :]
    return emb, s


def main():
    src = "corpus.txt"
    if not os.path.exists(src):
        print(f"ERROR: {src} no encontrado en el directorio actual.")
        return

    sents = leer_corpus(src)
    if not sents:
        print("No hay oraciones en el corpus para entrenar.")
        return

    print(f"Oraciones cargadas: {len(sents)}")
    M, vocab, inv_vocab = build_cooccurrence(sents, window=4)
    print(f"Vocabulario: {len(inv_vocab)}")

    emb, s = compute_svd_embeddings(M, n_components=100)
    modelos_dir = os.path.join("models")
    os.makedirs(modelos_dir, exist_ok=True)

    np.savez_compressed(os.path.join(modelos_dir, "embeddings_svd.npz"),
                        embeddings=emb, inv_vocab=inv_vocab)
    with open(os.path.join(modelos_dir, "vocab_svd.json"), "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

    print(f"Embeddings guardados en: {os.path.join(modelos_dir, 'embeddings_svd.npz')}")
    print(f"Primeras 10 palabras del vocab: {inv_vocab[:10]}")
    print(f"Top 8 valores singulares: {s[:8]}")


if __name__ == '__main__':
    main()
