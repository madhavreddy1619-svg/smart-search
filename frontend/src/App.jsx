import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const sectionId = (category) =>
    category.replaceAll(" ", "-").replaceAll("&", "and");

  const getProductIcon = (category) => {
    const text = category.toLowerCase();

    if (text.includes("desk")) return "🖥️";
    if (text.includes("chair") || text.includes("seating")) return "🪑";
    if (text.includes("coffee") || text.includes("tea")) return "☕";
    if (text.includes("snack")) return "🍫";
    if (text.includes("plate") || text.includes("cup")) return "🥤";
    if (text.includes("notebook") || text.includes("writing")) return "📓";
    if (text.includes("storage") || text.includes("filing")) return "🗂️";
    if (text.includes("projector") || text.includes("monitor")) return "🖥️";
    if (text.includes("cleaning")) return "🧼";
    if (text.includes("appliance")) return "🔌";
    if (text.includes("lighting") || text.includes("lamp")) return "💡";

    return "📦";
  };

  const handleSearch = async () => {
    setLoading(true);
    setResult(null);

    const response = await fetch("http://127.0.0.1:8000/smart-search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  const renderProducts = (products) => {
    if (!products || products.length === 0) {
      return <p className="empty">No products found.</p>;
    }

    return (
      <div className="products">
        {products.map((product) => (
          <div className="card" key={product.id}>
            <div className="image-placeholder">
              {getProductIcon(product.category)}
            </div>
            <h4>{product.name}</h4>
            <p>{product.category}</p>
            <strong>${product.price}</strong>
          </div>
        ))}
      </div>
    );
  };

  const totalProducts =
    result?.sections?.reduce(
      (total, section) => total + section.products.length,
      0
    ) || 0;

  return (
    <div className="page">
      <h1>Smart Search</h1>
      <p className="subtitle">Search by goal, product, brand, or occasion.</p>

      <div className="search-box">
        <input
          type="text"
          placeholder="Try: supplies for party of 30 people"
          value={query}
          autoFocus
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSearch();
            }
          }}
        />

        <button onClick={handleSearch} disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {loading && <div className="loading">Understanding your search...</div>}

      {result && (
        <div className="results">
          {result.cleaned_query &&
            result.cleaned_query !== result.query.toLowerCase() && (
              <p className="correction">
                Showing results for <strong>{result.cleaned_query}</strong>
              </p>
            )}

          {result.page_type === "guided_results" && (
            <>
              <div className="banner">
                <h2>{result.banner_headline}</h2>
                <p>{result.banner_subtitle}</p>
                <p>
                  <strong>
                    {totalProducts} products across {result.sections.length}{" "}
                    categories
                  </strong>
                </p>
              </div>

              <div className="chips">
                {result.sections.map((section) => (
                  <button
                    key={section.category}
                    onClick={() => {
                      document
                        .getElementById(sectionId(section.category))
                        ?.scrollIntoView({ behavior: "smooth" });
                    }}
                  >
                    {getProductIcon(section.category)} {section.category} (
                    {section.products.length})
                  </button>
                ))}
              </div>

              {result.sections.map((section) => (
                <div
                  className="section"
                  key={section.category}
                  id={sectionId(section.category)}
                >
                  <h3>
                    {getProductIcon(section.category)} {section.category} (
                    {section.products.length})
                  </h3>

                  <p className="search-query">
                    Search query: {section.search_query}
                  </p>

                  {renderProducts(section.products)}
                </div>
              ))}
            </>
          )}

          {result.intent === "keyword_product" && (
            <div className="banner">
              <h2>Showing results for "{result.cleaned_query}"</h2>
              <p>Standard product search.</p>
              {renderProducts(result.products)}
            </div>
          )}

          {result.intent === "brand_lookup" && (
            <div className="banner">
              <h2>Showing brand results for "{result.cleaned_query}"</h2>
              <p>Standard brand search.</p>
              {renderProducts(result.products)}
            </div>
          )}

          {result.intent === "zero_result_rescue" && (
            <div className="banner">
              <h2>We broadened your search for "{result.cleaned_query}"</h2>
              <p>No exact match found, so we used a broader search.</p>
              <p className="suggestions">
                We couldn't find an exact match, but here are some popular
                alternatives you may find useful.
              </p>
              {renderProducts(result.products)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;