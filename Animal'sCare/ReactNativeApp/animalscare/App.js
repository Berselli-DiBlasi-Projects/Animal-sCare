import React, { Component } from 'react';
import { Text, View, SafeAreaView, ScrollView, Image } from 'react-native';
import { createAppContainer } from 'react-navigation';
import * as Font from 'expo-font';
import Drawer from './components/DrawerNavigator';

const AppContainer = createAppContainer(Drawer);

export default class App extends React.Component {
  
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
