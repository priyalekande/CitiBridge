import React from 'react';
import { BrowserRouter, Route, Switch} from 'react-router-dom';  // npm install react-router-dom --save
import SecondPage from './components/upload';
import App from './components/login/App';

const Routes = () => (
    <BrowserRouter>
        <Switch>
            <Route path="/upload" component={SecondPage}/>
            <Route path="/" component={App}/>
        </Switch>
    </BrowserRouter>
);

export default Routes;