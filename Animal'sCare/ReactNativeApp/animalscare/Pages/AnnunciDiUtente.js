import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions, ActivityIndicator, FlatList, YellowBox } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import annuncio_default from '../assets/annuncio_default.jpg';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import {Picker} from 'native-base';
import { IconButton, ThemeProvider } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

class AnnunciDiUtente extends Component {

    user_id = -1;
    username = "";

    constructor(props){
        super(props);
        this.state ={ 
            isLoading: true
        }
    }
    
    componentDidMount() {
        this.user_id = this.props.navigation.state.params.user_id;
        this.username = this.props.navigation.state.params.username;
        this.fetchAnnunci();
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.setState({
                isLoading: true,
            }, function(){
    
            });
            this.user_id = this.props.navigation.state.params.user_id;
            this.username = this.props.navigation.state.params.username;
            this.fetchAnnunci();
          }
        );
    }

    componentWillUnmount() {
        this.willFocusSubscription.remove();
    }

    fetchAnnunci(){
        return fetch('http://2.224.160.133.xip.io/api/annunci/' + this.user_id + '/elenco/?format=json')

        .then((response) => response.json())
        .then((responseJson) => {

        this.setState({
            isLoading: false,
            dataSource: responseJson,
        }, function(){

        });
        })
        .catch((error) =>{
            this.fetchAnnunci();
        });
    }

    render() {

        if(this.state.isLoading){
            return(
                <View style={{flex: 1, paddingTop: height / 2}}>
                    <ActivityIndicator/>
                </View>
            )
        }

        YellowBox.ignoreWarnings([
            'VirtualizedLists should never be nested',
        ])
        
        return (
            
            <View style={styles.screen}>

                <View style={{alignSelf: 'flex-start', width: '100%', alignItems: 'center'}}>
                    <CustomHeader parent={this.props} />

                    <View style={styles.contentbar}>
                        <View style={styles.leftcontainer}>
                            <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                        </View>
                        <Text style={styles.title}>
                            Annunci di {this.username}
                        </Text>
                        <View style={styles.rightcontainer}>
                            <IconButton icon="filter" style={{paddingRight: 10}} onPress={this.ShowHidePickers} />
                        </View>
                    </View>
                </View>
                <View style={styles.flatlistview}>
                    <FlatList
                        style={{flex: 1}}
                        data={this.state.dataSource}
                        renderItem={({item, index}) => 
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: item.annuncio.id})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={ item.annuncio.logo_annuncio ? { uri: item.annuncio.logo_annuncio } : annuncio_default }
                                    style={styles.annuncioLogo}
                                />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.annuncioTitle} numberOfLines={1}>{item.annuncio.titolo}</Text>
                                    
                                    <Text style={styles.annuncioSubtitle} numberOfLines={2}>{item.annuncio.sottotitolo}</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Data: </Text>
                                        <Text>{item.annuncio.data_inizio} {item.annuncio.data_fine}</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Pubblicato da: </Text>
                                        <Text>{item.annuncio.user.username}</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>
                        }
                        keyExtractor={(item, index) => index.toString()}
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
    annuncioLogo: {
        width: 80,
        height: 80
    },
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    inputContainer: {
        flex: 1,
        minWidth: '96%',
        flexDirection: 'row'
    },
    annuncioTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        width: width - width / 2.6
    },
    annuncioSubtitle: {
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
        flex: 1,
        alignItems: 'center'
    },
    picker: {
        width: '100%',
        height: 40,
        backgroundColor: '#e7e7e7',
        borderColor: 'black',
        borderWidth: 3
    },
    pickerItem: {
        color: 'white'
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
    pickers: {
        height: 132,
        width: '90%',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    flatlistview: {
        flex: 1,
        width: '100%',
        justifyContent: 'space-between',
        alignItems: 'center'
    }
});

export default AnnunciDiUtente;