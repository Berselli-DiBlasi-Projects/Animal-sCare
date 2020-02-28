import React, { Component, createContext } from 'react';
import { Text, View, SafeAreaView, ScrollView, Image } from 'react-native';
import { createAppContainer } from 'react-navigation';
import * as Font from 'expo-font';
import Drawer from './components/DrawerNavigator';

const AppContainer = createAppContainer(Drawer);

export default class App extends React.Component {
  
  constructor() {
    super();
    global.logged_in = false;
    global.is_petsitter = false;
    global.user_key = '-1';
    global.username = '';
    global.user_id = -1;
  }

  state = {
    fontLoaded: false,
  };

  async componentDidMount() {
    await Font.loadAsync({
      'satisfy': require('./assets/fonts/satisfy.ttf'),
      'typold-medium': require('./assets/fonts/typold-medium.otf')
    });

    this.setState({ fontLoaded: true });
  }

  render () {
    if (!this.state.fontLoaded) {
      return (
        <View></View>
      );
    }

    return (
      <AppContainer navigation={this.props.navigation}/>
    );
  }
}
