import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, TextInput } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';
import CheckBox from 'react-native-check-box'
import PickerAnimali from '../components/PickerAnimali';

const {width, height} = Dimensions.get('window');

class ModificaAnnuncio extends Component {

    state = {
        chk1: false,
        chk2: false,
        chk3: false,
        chk4: false,
        chk5: false
    };

    render() {
        return (
                
            <View style={styles.screen}>
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Modifica annuncio
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
                                            <Text style={styles.textTitle}>Titolo:</Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Sottotitolo: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Descrizione: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Data inizio: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Data fine: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Pet: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Pet coins: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Logo annuncio: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Passeggiate: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Pulizia gabbia: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Ore compagnia: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Cibo: </Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Accompagna dal vet: </Text>
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
                                            <TextInput editable maxLength={245} multiline={true} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={20} multiline={true} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={20} multiline={true} />
                                        </View>
                                        <View>
                                            <PickerAnimali />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={10} multiline={true} />
                                        </View>
                                        <View>
                                            <TouchableOpacity style={styles.caricaStyle}>
                                                <Text style={{marginTop: 2}}>Browse...</Text>
                                            </TouchableOpacity>
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chk1'
                                                onClick={()=>{
                                                    this.setState({
                                                        chk1:!this.state.chk1
                                                    })
                                                }}
                                                isChecked={this.state.chk1}
                                            />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chk2'
                                                onClick={()=>{
                                                    this.setState({
                                                        chk2:!this.state.chk2
                                                    })
                                                }}
                                                isChecked={this.state.chk2}
                                            />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chk3'
                                                onClick={()=>{
                                                    this.setState({
                                                        chk3:!this.state.chk3
                                                    })
                                                }}
                                                isChecked={this.state.chk3}
                                            />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chk4'
                                                onClick={()=>{
                                                    this.setState({
                                                        chk4:!this.state.chk4
                                                    })
                                                }}
                                                isChecked={this.state.chk4}
                                            />
                                        </View>
                                        <View style={styles.checkBoxStyle}>
                                            <CheckBox
                                                title='chk5'
                                                onClick={()=>{
                                                    this.setState({
                                                        chk5:!this.state.chk5
                                                    })
                                                }}
                                                isChecked={this.state.chk5}
                                            />
                                        </View>
                                    </View>
                                </View>
                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Modifica annuncio" />
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
        marginBottom: 3,
        marginTop: 3,
        height: 28,
        width: 100,
        marginLeft: 10,
        borderWidth: 1,
        alignItems: 'center'
    },
    checkBoxStyle: {
        marginLeft: 10,
        marginBottom: 6,
        marginTop: 3
    },
    asteriskStyle: {
        marginLeft: 3,
        marginRight: 3,
        color: 'red'
    }
});

export default ModificaAnnuncio;