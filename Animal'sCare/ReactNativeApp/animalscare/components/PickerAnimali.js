import React, { Component } from 'react';
import { StyleSheet, Dimensions } from 'react-native';
import {Picker} from 'native-base';

const {width, height} = Dimensions.get('window');

export default class PickerAnimali extends Component {

    state = {
        pet: "cane"
    };

    render() {
        return (
            <Picker
                style={styles.picker} itemStyle={styles.pickerItem}
                selectedValue={this.state.pet}
                onValueChange={(itemValue) => this.setState({pet: itemValue})}
                >
                <Picker.Item label="Cane" value="cane" />
                <Picker.Item label="Gatto" value="gatto" />
                <Picker.Item label="Coniglio" value="coniglio" />
                <Picker.Item label="Volatile" value="volatile" />
                <Picker.Item label="Rettile" value="rettile" />
                <Picker.Item label="Altro" value="altro" />
            </Picker>
        );
    }
}

const styles = StyleSheet.create({
    picker: {
        marginLeft: 10,
        width: width - width / 2,
        height: 28,
        backgroundColor: '#e7e7e7',
        marginBottom: 3,
        marginTop: 3
    },
    pickerItem: {
        color: 'white'
    }
});