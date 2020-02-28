import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions, ActivityIndicator, FlatList } from 'react-native';
import SearchBar from "react-native-dynamic-search-bar";
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import profilo_default from '../assets/user_default.jpg';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

class CercaUtente extends Component {

    constructor(props){
        super(props);
        this.state ={ 
            isLoading: false,
            search: '',
            dataSource: null
        }
    }
    
    fetchCercaUtente(text) {
        if(text == "") {
            this.setState({
                isLoading: false,
            }, function(){

            });
        } else {
            return fetch('http://2.224.160.133.xip.io/api/utenti/cerca/' + text + '/?format=json')
            .then((response) => response.json())
            .then((responseJson) => {

            this.setState({
                dataSource: responseJson,
                isLoading: false,
            }, function(){

            });

            })
            .catch((error) =>{
            this.fetchCercaUtente(text);
            });
        }
    }

    render() {

        if(this.state.isLoading){
            return(
                <View style={{flex: 1, paddingTop: height / 2}}>
                    <ActivityIndicator/>
                </View>
            )
        }

        return (
            
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Cerca utente
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>

                <SearchBar
                    onPressToFocus
                    autoFocus={false}
                    fontColor="#c6c6c6"
                    iconColor="#c6c6c6"
                    shadowColor="#282828"
                    cancelIconColor="#c6c6c6"
                    backgroundColor="#36485f"
                    placeholder="Cerca username"
                    width="88%"
                    activeOpacity={.9}
                    onChangeText={text => {
                        this.fetchCercaUtente(text);
                    }}
                    onPressCancel={() => {
                        console.log("cancel");
                    }}
                />

                <View style={{paddingBottom: 5}}></View>

                <View style={styles.flatlistview}>
                    <FlatList
                        style={{flex: 1}}
                        data={this.state.dataSource}
                        renderItem={({item}) => 
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('ProfiloUtente', {user_id: item.user.id})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={ item.foto_profilo ? { uri: item.foto_profilo } : profilo_default }
                                     style={styles.profileLogo}  />
                                </View>
                                <View style={styles.data}>
                                    <Text style={styles.profileName} numberOfLines={1}>{item.user.first_name} {item.user.last_name}</Text>
                                    
                                    <Text style={styles.profileData} numberOfLines={2}>{item.pet_sitter == true ? 'Petsitter' : 'Utente normale'},
                                         {item.indirizzo}, {item.citta}</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto medio: </Text>
                                        <Text>5/5</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Recensioni ricevute: </Text>
                                        <Text>1</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>
                        }
                        keyExtractor={({id}, index) => id.toString()}
                    />
                </View>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        alignItems: 'center'
    },
    profileLogo: {
        width: 80,
        height: 80
    },
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    inputContainer: {
        minWidth: '96%',
        flexDirection: 'row'
    },
    profileName: {
        fontSize: 18,
        fontWeight: 'bold',
        width: width - width / 2.6
    },
    profileData: {
        width: width - width / 2.6
    },
    data: {
        flex: 1
    },
    image: {
        paddingRight: 10
    },
    textInline: {
        flexDirection: 'row'
    },
    touchableopacity: {
        alignItems: 'center'
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
    flatlistview: {
        flex: 1,
        width: '100%',
        justifyContent: 'space-between',
        alignItems: 'center'
    }
});

export default CercaUtente;