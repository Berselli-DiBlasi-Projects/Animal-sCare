import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions, ActivityIndicator, YellowBox, FlatList } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');


class RecensioniRicevute extends Component {

    username = "";

    constructor(props){
        super(props);
        this.state ={ 
            isLoading: true
        }
    }
    
    componentDidMount() {
        this.username = this.props.navigation.state.params.username;
        this.fetchRecensioni();
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.setState({
                isLoading: true,
            }, function(){
    
            });
            this.username = this.props.navigation.state.params.username;
            this.fetchRecensioni();
          }
        );
    }

    componentWillUnmount() {
        this.willFocusSubscription.remove();
    }

    fetchRecensioni(){
    return fetch('http://2.224.160.133.xip.io/api/recensioni/ricevute/' 
        + this.username + '/?format=json')

        .then((response) => response.json())
        .then((responseJson) => {

        this.setState({
            isLoading: false,
            dataSource: responseJson,
        }, function(){

        });
        })
        .catch((error) =>{
            this.fetchRecensioni();
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
                            Recensioni di {this.username}
                        </Text>
                        <View style={styles.rightcontainer}></View>
                    </View>
                </View>
                <View style={styles.flatlistview}>
                    <FlatList
                        style={{flex: 1}}
                        data={this.state.dataSource}
                        renderItem={({item, index}) => 
                            <Card style={styles.inputContainer}>
                                <View style={styles.data}>
                                    <Text style={styles.recensioneTitle} numberOfLines={1}>{item.titolo}</Text>
                                    
                                    <Text style={styles.recensioneSubtitle} numberOfLines={2}>{item.descrizione}</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto: </Text>
                                        <Text>{item.voto}</Text>
                                    </View>
                                </View>
                            </Card>
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
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    inputContainer: {
        minWidth: '96%',
        flexDirection: 'row'
    },
    recensioneTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        width: width - width / 2.6
    },
    recensioneSubtitle: {
        width: width - width / 2.6
    },
    data: {
        flex: 1
    },
    flatlistview: {
        flex: 1,
        width: '100%',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    textInline: {
        flexDirection: 'row'
    }
});

export default RecensioniRicevute;