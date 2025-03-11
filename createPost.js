import React, { useState } from 'react';
import { useRouter } from 'next/router';

const CreatePost = () => {
  const [postContent, setPostContent] = useState('');
  const router = useRouter();

  const handlePost = (e) => {
    e.preventDefault();
    const existingPosts = JSON.parse(localStorage.getItem('posts')) || [];
    existingPosts.push(postContent);
    localStorage.setItem('posts', JSON.stringify(existingPosts));
    router.push('/');
  };

  return (
    <div>
      <h1>إنشاء منشور جديد</h1>
      <form onSubmit={handlePost}>
        <textarea
          placeholder="اكتب منشورك هنا..."
          value={postContent}
          onChange={(e) => setPostContent(e.target.value)}
        />
        <button type="submit">نشر</button>
      </form>
    </div>
  );
};

export default CreatePost;
