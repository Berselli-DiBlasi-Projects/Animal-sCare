import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Header } from 'react-native-elements';
import { Icon } from 'native-base';

const CustomHeader = props => {
    return (
        <Header
            leftComponent={<Icon name="menu" style={{color: '#e1e1e1'}} onPress={() => props.parent.navigation.openDrawer()} />}
            centerComponent={{ text: 'Animal\'s Care', style: { color: '#e1e1e1', fontFamily: 'satisfy', fontSize: 18 } }}
            containerStyle={{
                backgroundColor: '#232f3e',
                justifyContent: 'space-around',
            }}
            rightComponent={<Icon name="home" style={{color: '#e1e1e1'}} onPress={() => props.parent.navigation.navigate('ListaAnnunci')} />}
        />
    );
};

export default CustomHeader;