import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, TextInput } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';
import PickerAnimali from '../components/PickerAnimali';
import PickerProvince from '../components/PickerProvince';
import PickerRegioni from '../components/PickerRegioni';

const {width, height} = Dimensions.get('window');

class ModificaProfiloNormale extends Component {

    render() {
        return (
                
            <View style={styles.screen}>
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Modifica profilo (normale)
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>

                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={{alignItems: 'center'}}>
                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <View style={{flexDirection: 'row'}}>
                                    <View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Username:</Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Password: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Conferma password: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Nome: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Cognome: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Email: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Indirizzo: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Città: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Provincia: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Regione: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Telefono: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Foto profilo: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Nome pet: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Pet: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Razza: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Età: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Caratteristiche: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Foto pet: </Text>
                                        </View>
                                    </View>

                                    <View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <PickerProvince />
                                        <PickerRegioni />
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View>
                                            <TouchableOpacity style={styles.caricaStyle}>
                                                <Text style={{marginTop: 2}}>Browse...</Text>
                                            </TouchableOpacity>
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <PickerAnimali />
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95} />
                                        </View>
                                        <View>
                                            <TouchableOpacity style={styles.caricaStyle}>
                                                <Text style={{marginTop: 2}}>Browse...</Text>
                                            </TouchableOpacity>
                                        </View>
                                    </View>
                                </View>
                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Registrati" />
                                    </View>
                                </View>

                                <View style={{flexDirection: 'row', marginTop: 20, marginBottom: 5}}>
                                    <Text>I campi contrassegnati con</Text>
                                    <Text style={styles.asteriskStyle}>*</Text>
                                    <Text>sono obbligatori.</Text>

                                </View>
                            </View>
                        </Card>
                    </View>
                </ScrollView>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    screen: {
        flex: 1
    },
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    buttonview: {
        width: 110,
        paddingRight: 5,
        paddingLeft: 5
    },
    inputContainer: {
        minWidth: '96%'
    },
    controlli: {
        paddingTop: 20,
        paddingRight: 5,
        alignItems: 'center'
    },
    data: {
        paddingTop: 20,
        paddingLeft: 10
    },
    entryTitle: {
        marginBottom: 5,
        marginTop: 9,
        flexDirection: 'row'
    },
    textTitle: {
        fontWeight: 'bold'
    },
    contentbar: {
        height: 50,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center'
      },
    leftcontainer: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'flex-start'
    },
    rightcontainer: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'flex-end',
        alignItems: 'center'
    },
    textContainer: {
        borderWidth: 1,
        height: 28,
        width: width - width / 2,
        marginLeft: 10,
        marginBottom: 3,
        marginTop: 3
    },
    caricaStyle: {
        marginBottom: 1,
        marginTop: 1,
        height: 28,
        width: 100,
        marginLeft: 10,
        borderWidth: 1,
        alignItems: 'center'
    },
    asteriskStyle: {
        marginLeft: 3,
        marginRight: 3,
        color: 'red'
    }
});

export default ModificaProfiloNormale;