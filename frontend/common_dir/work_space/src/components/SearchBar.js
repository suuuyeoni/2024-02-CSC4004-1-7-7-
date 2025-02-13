//필요한 모듈 import
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // React Router에서 useNavigate 가져오기
import styles from './SearchBar.module.css';
import { debounce } from "lodash";
import searchIcon from "../assets/img/search.png";

const SearchBar = ({ onSearch }) => {
  //필요한 변수 설정
  const [searchTerm, setSearchTerm] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  //입력에 따른 변화 check
  const handleChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    fetchSuggestions(value);
  };
  const handleSearch = () => { if (onSearch) onSearch(searchTerm); };

  // 클릭한 가게의 id로 상세 페이지로 이동
  const handleSuggestionClick = (id) => {
    navigate(`/details/${id}`); // 해당 id로 이동
  };

  // Debounced 검색 함수
  const fetchSuggestions = debounce(async (query) => {
    if (!query) {
      setSuggestions([]);
      return;
    }
    setLoading(true);

    try {
      //http://34.47.82.254:8000/api/autoComplete/?query=${encodeURIComponent(query)} --> 실제 서버 주소
      //http://localhost:8000/api/autoComplete/?query=${encodeURIComponent(query)}  --> 로컬 환경 테스트
      const response = await fetch(`http://34.47.82.254:8000/api/autoComplete/?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      //콘솔로 결과 check
      console.log("Suggestions received:", data);
      // results 배열만 설정
      setSuggestions(data.results || []);
    } catch (error) {
      console.error("Error fetching suggestions:", error.message);
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  }, 300);

  //콘솔로 결과 check
  useEffect(() => {
    console.log("Current suggestions:", suggestions);
  }, [suggestions]);

  //구현부
  return (
    <div className={styles.search_bar_wrapper}>
      <input
        type="text"
        placeholder="Search for..."
        value={searchTerm}
        onChange={handleChange}
        className={styles.search_input}
      />

      <div className={styles.search_button}>
        <img src={searchIcon} alt="Search" className={styles.search_icon} />
      </div>

      {loading && <div className={styles.loading}>Loading...</div>}

      {suggestions.length > 0 && (
        <ul className={styles.suggestions_list}>
          {suggestions.map((item) => (
            <li
              key={item.id}
              className={styles.suggestion_item}
              onClick={() => handleSuggestionClick(item.id)} // 클릭 시 id로 이동
            >
              {item.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBar;
