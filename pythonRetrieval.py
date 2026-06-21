import os, json, math
from pathlib import Path
from typing import List, Dict

CHUNK_SIZE = 120
OVERLAP = 20

class KrakowRetriever:
    def __init__(self, data_path: str = 'locations.json'):
        self.data_path = Path(data_path)
        self.docs: List[Dict] = []
        self.bm25_index: Dict[str, List[int]] = {}
        self._idf: Dict[str, float] = {}
        self._tfidf_vecs: List[Dict[str, float]] = []
        self._load_or_build()

    def _load_or_build(self):
        if self.data_path.exists():
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.docs = json.load(f)
            if not self.docs:
                self._seed_demo()
        else:
            self._seed_demo()
        for idx, doc in enumerate(self.docs):
            terms = (doc.get('title','') + ' ' + ' '.join(doc.get('tags',[]))).lower().split()
            for t in set(terms):
                self.bm25_index.setdefault(t, []).append(idx)
        self._build_tfidf()

    def _seed_demo(self):
        locations = [
          {"title": "Wawel Castle", "tags": ["castle","royal","UNESCO"], "text": "Wawel Castle is a royal castle and museum in Krakow, Poland. It was the seat of Polish kings for centuries."},
          {"title": "Main Market Square", "tags": ["square","old town","shops"], "text": "The Main Market Square in Krakow is one of the largest medieval town squares in Europe, bustling with cafes and shops."},
          {"title": "St. Mary's Basilica", "tags": ["church","bugle","basilica"], "text": "St. Mary's Basilica is famous for its Hejnal bugle call played every hour from the taller tower."},
          {"title": "Kazimierz District", "tags": ["jewish","district","culture"], "text": "Kazimierz is the historic Jewish district of Krakow, known for synagogues, street art, and vibrant nightlife."},
          {"title": "Wieliczka Salt Mine", "tags": ["salt","mine","UNESCO"], "text": "The Wieliczka Salt Mine is a UNESCO World Heritage Site near Krakow with chapels carved from salt rock."},
          {"title": "Planty Park", "tags": ["park","green","walk"], "text": "Planty is a ring of green space surrounding Krakow's Old Town, perfect for walking and jogging."},
          {"title": "Cloth Hall", "tags": ["market","souvenirs","renaissance"], "text": "The Cloth Hall in the center of Main Square offers souvenirs and reflects Krakow's Renaissance trading heritage."},
          {"title": "Wawel Cathedral", "tags": ["church","crypt","royal"], "text": "Wawel Cathedral is the coronation church of Polish monarchs, located on Wawel Hill next to the Castle."},
          {"title": "Schindler Factory", "tags": ["museum","WWII","factory"], "text": "Oskar Schindler's Enamel Factory is now a museum about Krakow during World War II."},
          {"title": "Rynek Underground", "tags": ["museum","medieval","underground"], "text": "Rynek Underground is a modern museum beneath the Main Market Square showing Krakow's medieval trade routes."}
        ]
        text = "\n".join(x["text"] for x in locations)
        self.docs = []
        for loc in locations:
            body = loc["text"]
            start = 0
            while start < len(body):
                chunk = body[start:start+CHUNK_SIZE]
                self.docs.append({
                    "title": loc["title"],
                    "tags": loc.get("tags", []),
                    "text": chunk,
                    "source": loc["title"],
                    "uri": f"krakow://{loc['title'].lower().replace(' ','-')}"
                })
                start += max(1, CHUNK_SIZE - OVERLAP)
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(self.docs, f, ensure_ascii=False, indent=2)

    def _build_tfidf(self):
        N = len(self.docs)
        for term, doc_ids in self.bm25_index.items():
            self._idf[term] = math.log((N + 1) / (len(doc_ids) + 1)) + 1
        self._tfidf_vecs: List[Dict[str, float]] = []
        for doc in self.docs:
            vec = {}
            terms = (doc.get('title','') + ' ' + doc.get('text','')).lower().split()
            for t in terms:
                vec[t] = vec.get(t, 0) + 1
            for t, tf in vec.items():
                vec[t] = tf * self._idf.get(t, 0)
            self._tfidf_vecs.append(vec)

    @staticmethod
    def _cosine(a: Dict[str,float], b: Dict[str,float]) -> float:
        dot = sum(a[k]*b.get(k,0) for k in a)
        na = math.sqrt(sum(v*v for v in a.values()))
        nb = math.sqrt(sum(v*v for v in b.values()))
        return dot/(na*nb) if na and nb else 0.0

    def _query_vec(self, q: str) -> Dict[str,float]:
        terms = q.lower().split()
        qtf = {t: terms.count(t) for t in set(terms)}
        return {t: c * self._idf.get(t,0) for t,c in qtf.items()}

    def retrieve(self, query: str, k: int = 4) -> List[Dict]:
        qv = self._query_vec(query)
        scored = []
        terms = query.lower().split()
        for idx, (vec, doc) in enumerate(zip(self._tfidf_vecs, self.docs)):
            bm25_hits = sum(1 for t in terms if t in self.bm25_index and idx in self.bm25_index[t])
            hybrid = 0.6 * self._cosine(qv, vec) + 0.4 * min(bm25_hits / max(1, len(terms)), 1.0)
            scored.append((hybrid, idx))
        scored.sort(reverse=True)
        return [self.docs[i] for _, i in scored[:k]]

retriever = KrakowRetriever()

if __name__ == '__main__':
    for q in ['castle', 'UNESCO near Krakow', 'good for walking', 'Jewish heritage']:
        hits = retriever.retrieve(q)
        print('QUERY:', q)
        for h in hits:
            print(' ', h['source'], '|', h['text'][:60])
