import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import UserInfo from './urls/user_info/user_info.js';

import { BrowserRouter, Route, Routes } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
    <BrowserRouter>
        <Routes>
            <Route path='/user/*' element={<UserInfo />} />
        </Routes>
    </BrowserRouter>
);
