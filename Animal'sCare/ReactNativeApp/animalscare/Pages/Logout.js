import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { Dimensions } from 'react-native';

const {width, height} = Dimensions.get('window');

class Logout extends Component {

    componentDidMount() {
        this.logoutExecute();
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.logoutExecute();
          }
        );
    }

    componentWillUnmount() {
    this.willFocusSubscription.remove();
    }

    logoutExecute() {
        global.logged_in = false;
        global.user_key = '-1';
        global.username = '';
        global.user_id = -1;
        this.props.navigation.goBack(null);
    }

    render() {
        return null;
    }
}

export default Logout;