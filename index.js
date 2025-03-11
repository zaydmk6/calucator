import { useEffect, useState } from 'react';
import styles from '../styles/Home.module.css';
import PostCard from '../components/PostCard';

const Home = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const storedPosts = JSON.parse(localStorage.getItem('posts')) || [];
    setPosts(storedPosts);
  }, []);

  return (
    <div className={styles.container}>
      <h1>مرحبًا بك في موقع التواصل الاجتماعي!</h1>
      <div>
        {posts.length === 0 ? (
          <p>لا توجد مشاركات حالياً.</p>
        ) : (
          posts.map((post, index) => (
            <PostCard key={index} content={post} />
          ))
        )}
      </div>
    </div>
  );
};

export default Home;
