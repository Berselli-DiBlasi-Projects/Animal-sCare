import React, { Component } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import CustomHeader from '../components/Header';

class Contattaci extends Component {

    render() {
        return (
            <View style={styles.screen}>
                <CustomHeader parent={this.props} />
                
                <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
                    <Text>Pagina Contattaci</Text>
                </View>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    screen: {
        flex: 1
    }
});

export default Contattaci;