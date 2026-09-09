import { useState } from "react";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const popularSearches = [
    "Set up a home office",
    "Supplies for a party of 30",
    "New hire desk setup for 10",
    "Stock an office break room",
  ];

  const sectionId = (category = "") =>
    category
      .toLowerCase()
      .replaceAll("&", "and")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");

  const getProductIcon = (category = "") => {
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
    if (text.includes("printer")) return "🖨️";
    if (text.includes("paper")) return "📄";
    if (text.includes("technology") || text.includes("accessory")) return "⌨️";

    return "📦";
  };

  const handleSearch = async (searchValue = query) => {
    const trimmedQuery = searchValue.trim();

    if (!trimmedQuery) {
      setError("Please enter a product, brand, goal, or occasion.");
      return;
    }

    setQuery(trimmedQuery);
    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/smart-search`,
         {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: trimmedQuery }),
      }
    );

      if (!response.ok) {
        throw new Error(`Search failed with status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (requestError) {
      console.error("Smart Search error:", requestError);

      setError(
        "We could not complete your search. Make sure the backend server is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    handleSearch(suggestion);
  };

  const renderProducts = (products) => {
    if (!products || products.length === 0) {
      return (
        <div className="empty-state">
          <span>🔎</span>
          <p>No products were found in this category.</p>
        </div>
      );
    }

    return (
      <div className="products">
        {products.map((product) => (
          <article className="card" key={product.id}>
            <div className="product-image">
              <span>{getProductIcon(product.category)}</span>
            </div>

            <div className="product-details">
              <span className="product-category">{product.category}</span>

              <h4>{product.name}</h4>

              <div className="product-footer">
                <strong>
                  ${Number(product.price).toFixed(2)}
                </strong>
              </div>
            </div>
          </article>
        ))}
      </div>
    );
  };

  const totalProducts =
    result?.sections?.reduce(
      (total, section) => total + (section.products?.length || 0),
      0
    ) || 0;

  const showCorrection =
    result?.cleaned_query &&
    result?.query &&
    result.cleaned_query.toLowerCase() !== result.query.toLowerCase();

  return (
    <div className="app-shell">
      <div className="background-decoration background-decoration-one" />
      <div className="background-decoration background-decoration-two" />
      <div className="background-decoration background-decoration-three" />
      <div className="background-grid" />

      <header className="site-header">
        <a href="/" className="brand">
          <span className="brand-icon">✦</span>

          <span>
            <strong>Smart Search</strong>
            <small>AI Shopping Assistant</small>
          </span>
        </a>

        <nav className="header-nav" aria-label="Main navigation">
          <a href="#search">Search</a>
          <a href="#results">Recommendations</a>
          <button type="button" className="account-button">
            My Account
          </button>
        </nav>
      </header>

      <main className="page">
        <section className="hero" id="search">
          <div className="hero-badge">
            <span>✦</span>
            AI-powered product discovery
          </div>

          <h1>
            Find everything you need
            <span> in one smart search.</span>
          </h1>

          <p className="subtitle">
            Describe a goal, product, brand, workspace, or event. Smart Search
            organizes the right products for you.
          </p>

          <div className="search-panel">
            <div className="search-box">
              <span className="search-icon" aria-hidden="true">
                ⌕
              </span>

              <input
                type="text"
                placeholder="Try: supplies for a party of 30 people"
                value={query}
                autoFocus
                aria-label="Search products"
                onChange={(event) => {
                  setQuery(event.target.value);
                  setError("");
                }}
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !loading) {
                    handleSearch();
                  }
                }}
              />

              <button
                type="button"
                className="search-button"
                onClick={() => handleSearch()}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="button-spinner" />
                    Searching
                  </>
                ) : (
                  <>
                    <span>✦</span>
                    Smart Search
                  </>
                )}
              </button>
            </div>

            {error && (
              <div className="error-message" role="alert">
                <span>!</span>
                {error}
              </div>
            )}

            <div className="popular-searches">
              <span className="popular-label">Popular searches:</span>

              <div className="suggestion-list">
                {popularSearches.map((suggestion) => (
                  <button
                    type="button"
                    key={suggestion}
                    disabled={loading}
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="hero-benefits">
            <div>
              <span>🧠</span>
              <p>
                <strong>Understands intent</strong>
                Recognizes goals and occasions
              </p>
            </div>

            <div>
              <span>🗂️</span>
              <p>
                <strong>Organizes products</strong>
                Groups results by category
              </p>
            </div>

            <div>
              <span>⚡</span>
              <p>
                <strong>Saves time</strong>
                Completes your list faster
              </p>
            </div>
          </div>
        </section>

        {loading && (
          <section className="loading-panel" aria-live="polite">
            <div className="ai-loader">
              <span />
              <span />
              <span />
            </div>

            <div>
              <strong>Understanding your search</strong>
              <p>
                Identifying your goal and finding relevant product categories.
              </p>
            </div>
          </section>
        )}

        {result && (
          <section className="results" id="results">
            {showCorrection && (
              <div className="correction">
                <span>✓</span>
                Showing results for{" "}
                <strong>{result.cleaned_query}</strong>
              </div>
            )}

            {result.page_type === "guided_results" && (
              <>
                <div className="results-banner">
                  <div className="banner-content">
                    <div className="banner-icon">✨</div>

                    <div>
                      <span className="eyebrow">Smart Search understood</span>
                      <h2>{result.banner_headline}</h2>
                      <p>{result.banner_subtitle}</p>
                    </div>
                  </div>

                  <div className="result-summary">
                    <div>
                      <strong>{totalProducts}</strong>
                      <span>Products</span>
                    </div>

                    <div>
                      <strong>{result.sections?.length || 0}</strong>
                      <span>Categories</span>
                    </div>
                  </div>
                </div>

                <div className="category-navigation">
                  <div>
                    <span className="navigation-label">Jump to category</span>

                    <div className="chips">
                      {result.sections?.map((section) => (
                        <button
                          type="button"
                          key={section.category}
                          onClick={() => {
                            document
                              .getElementById(sectionId(section.category))
                              ?.scrollIntoView({
                                behavior: "smooth",
                                block: "start",
                              });
                          }}
                        >
                          <span>{getProductIcon(section.category)}</span>
                          {section.category}
                          <small>{section.products?.length || 0}</small>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="section-list">
                  {result.sections?.map((section) => (
                    <section
                      className="product-section"
                      key={section.category}
                      id={sectionId(section.category)}
                    >
                      <div className="section-header">
                        <div>
                          <div className="section-title">
                            <span className="section-icon">
                              {getProductIcon(section.category)}
                            </span>

                            <div>
                              <h3>{section.category}</h3>
                              <p>
                                {section.products?.length || 0} recommended
                                products
                              </p>
                            </div>
                          </div>
                        </div>

                        {section.search_query && (
                          <span className="search-query">
                            Search: {section.search_query}
                          </span>
                        )}
                      </div>

                      {renderProducts(section.products)}
                    </section>
                  ))}
                </div>
              </>
            )}

            {result.intent === "keyword_product" && (
              <div className="standard-results">
                <div className="standard-results-header">
                  <span className="result-type-icon">🔎</span>

                  <div>
                    <span className="eyebrow">Product search</span>
                    <h2>
                      Results for “{result.cleaned_query}”
                    </h2>
                    <p>
                      Products matching your search request.
                    </p>
                  </div>
                </div>

                {renderProducts(result.products)}
              </div>
            )}

            {result.intent === "brand_lookup" && (
              <div className="standard-results">
                <div className="standard-results-header">
                  <span className="result-type-icon">🏷️</span>

                  <div>
                    <span className="eyebrow">Brand search</span>
                    <h2>
                      Brand results for “{result.cleaned_query}”
                    </h2>
                    <p>
                      Products available from the selected brand.
                    </p>
                  </div>
                </div>

                {renderProducts(result.products)}
              </div>
            )}

            {result.intent === "zero_result_rescue" && (
              <div className="standard-results rescue-results">
                <div className="standard-results-header">
                  <span className="result-type-icon">🧭</span>

                  <div>
                    <span className="eyebrow">Broadened search</span>
                    <h2>
                      Alternatives for “{result.cleaned_query}”
                    </h2>
                    <p>
                      We could not find an exact match, so we selected related
                      products that may still help.
                    </p>
                  </div>
                </div>

                {renderProducts(result.products)}
              </div>
            )}
          </section>
        )}
      </main>

      <footer className="site-footer">
        <div className="footer-brand">
          <span className="brand-icon">✦</span>
          Smart Search AI
        </div>

        <p>
          Intelligent product discovery powered by natural-language search.
        </p>
      </footer>
    </div>
  );
}

export default App;