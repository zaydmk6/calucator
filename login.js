import React, { useState } from 'react';
import { useRouter } from 'next/router';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = (e) => {
    e.preventDefault();
    if (username && password) {
      // تخزين اسم المستخدم في localStorage عند تسجيل الدخول
      localStorage.setItem('username', username);
      router.push('/');
    } else {
      alert('يرجى إدخال جميع البيانات');
    }
  };

  return (
    <div>
      <h1>تسجيل الدخول</h1>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="اسم المستخدم"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="كلمة المرور"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">دخول</button>
      </form>
    </div>
  );
};

export default Login;
