import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, TextInput } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card'
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import { Dimensions } from 'react-native';
import { IconButton } from 'react-native-paper';
import { Picker } from 'native-base';

const {width, height} = Dimensions.get('window');

class NuovaRecensione extends Component {

    constructor(props){
        super(props);
        this.state ={ 
            titolo: "",
            descrizione: "",
            voto: 1,
            error_message: ""
        }
    }

    inviaRecensione = () => {
        if (this.state.titolo != "" && this.state.descrizione != "") {
            fetch('http://2.224.160.133.xip.io/api/recensioni/nuova/' + this.props.navigation.state.params.username + '/',
            {
              method: 'POST',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + global.user_key,
              },
              body: JSON.stringify({
                titolo: this.state.titolo,
                descrizione: this.state.descrizione,
                voto: this.state.voto
              }),
            })
            .then(res => res.json())
            .then((res) => {
                if (res.id != null) {
                    this.clearFields();
                    this.props.navigation.goBack(null);
                } else {
                    this.setState({error_message: JSON.stringify(res)});
                }
            })
            .catch((error) => {
                this.setState({error_message: error});
                this.inviaRecensione;
            })
        } else {
            this.setState({error_message: "Errore: assicurati di riempire tutti i campi."});
        }
    }

    clearFields = () => {
        this.setState({titolo: ""});
        this.setState({descrizione: ""});
        this.setState({voto: 1});
        this.setState({error_message: ""});
        this.txtTitolo.clear();
        this.txtDescrizione.clear();
    }

    render() {
        return (
                
            <View style={styles.screen}>
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Recensisci utente
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
                                            <Text style={styles.textTitle}>Descrizione: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                        <View style={styles.entryTitle}>
                                            <Text style={styles.textTitle}>Voto: </Text>
                                            <Text style={styles.asteriskStyle}>*</Text>
                                        </View>
                                    </View>

                                    <View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={95}
                                            ref={input => { this.txtTitolo = input }}
                                            onChangeText={(value) => this.setState({titolo: value})} />
                                        </View>
                                        <View style={styles.textContainer}>
                                            <TextInput editable maxLength={300} 
                                            ref={input => { this.txtDescrizione = input }}
                                            onChangeText={(value) => this.setState({descrizione: value})}/>
                                        </View>
                                        <Picker
                                            style={styles.picker} itemStyle={styles.pickerItem}
                                            selectedValue={this.state.voto}
                                            onValueChange={(itemValue) => this.setState({voto: itemValue})}
                                            >
                                            <Picker.Item label="1" value={1} />
                                            <Picker.Item label="2" value={2} />
                                            <Picker.Item label="3" value={3} />
                                            <Picker.Item label="4" value={4} />
                                            <Picker.Item label="5" value={5} />
                                        </Picker>
                                    </View>
                                </View>
                                <View style={styles.controlli}>
                                    <View style={styles.buttonview}>
                                        <Button title="Invia recensione" onPress={ this.inviaRecensione } />
                                    </View>
                                </View>

                                <View style={{paddingTop: 15}}></View>
                                <Text style={{color: 'red'}}>{this.state.error_message}</Text>

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
    asteriskStyle: {
        marginLeft: 3,
        marginRight: 3,
        color: 'red'
    },
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

export default NuovaRecensione;