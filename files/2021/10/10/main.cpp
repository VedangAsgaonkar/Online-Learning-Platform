#include <iostream>
#include "network.cpp"

using namespace std;

class Packet_dispatcher{
	Node* net[1000];
	int curr_point;
public: 
	Packet_dispatcher(){
		curr_point = 0;
	}
	void insert(Node* x){
		net[curr_point]= x;
		int l = curr_point;
		while( l >= 1 && (net[(l-1)/2]->next_dispatch()) > (net[l]->next_dispatch())){
			swap(net[(l-1)/2],net[l]);
			l = (l-1)/2;
		}
		curr_point++;
	}
	void print(){
		for(int i =0 ; i<curr_point ; i++){
			cout<<(net[i]->next_dispatch())<<" ";
		}
		cout<<endl;
	}
	float min(){
		if(curr_point > 0)return net[0]->next_dispatch();
		else return 100000.00;
	}

	void heapify(int a){
		if(2*a+1 > curr_point-1)return;
		else if(2*a+2 == curr_point){
			if((net[2*a+1]->next_dispatch())<(net[a]->next_dispatch())){
				swap(net[2*a+1],net[a]);
			}
			return;
		}
		else if((net[2*a+1]->next_dispatch() >= net[a]->next_dispatch()) && (net[2*a+2]->next_dispatch()>= net[a]->next_dispatch()))return;
		else{
			if(net[2*a+1]->next_dispatch() >= net[2*a+2]->next_dispatch()){
				swap(net[2*a+2], net[a]);
				heapify(2*a+2);
			}
			else{
				swap(net[2*a+1],net[a]);
				heapify(2*a+1);
			}
		}
	}
	Node* delete_min(){
		curr_point--;
		swap(net[0],net[curr_point]);
		heapify(0);
		return net[curr_point];
	}
};
class Packet_arrival{
	Packet* pac[1000];
	int curr_point;
public: 
	Packet_arrival(){
		curr_point = 0;
	}
	void insert(Packet* x){
		pac[curr_point]=x;
		if(curr_point == 1){
			pac[curr_point]->errored = 1;
			pac[0]->errored = 1;
		}
		else if(curr_point > 1){
			pac[curr_point]->errored = 1;
		}
		int l = curr_point;
		while( l >= 1 && pac[(l-1)/2]->time_recieved > pac[l]->time_recieved){
			swap(pac[(l-1)/2],pac[l]);
			l = (l-1)/2;
		}
		curr_point++;
	}

	void print(){
		for(int i =0 ; i<curr_point ; i++){
			cout<<pac[i]->time_recieved<<" ";
		}
		cout<<endl;
	}
	void printmsg(){
		if(curr_point>1)cout<<"Previous packet was with errors"<<endl;
		else cout<<"Error free packet"<<endl;
	}
	float min(){
		if(curr_point>0)return pac[0]->time_recieved;
		else return 100000.00;
	}

	void heapify(int a){
		if(2*a+1 > curr_point-1)return;
		else if(2*a+2 == curr_point){
			if(pac[2*a+1]->time_recieved<pac[a]->time_recieved){
				swap(pac[2*a+1],pac[a]);
			}
			return;
		}
		else if(pac[2*a+1]->time_recieved >= pac[a]->time_recieved && pac[2*a+2]->time_recieved>= pac[a]->time_recieved)return;
		else{
			if(pac[2*a+1]->time_recieved >= pac[2*a+2]->time_recieved){
				
				swap(pac[2*a+2],pac[a]);
				heapify(2*a+2);
			}
			else{
				swap(pac[2*a+1],pac[a]);
				heapify(2*a+1);
			}
		}
	}
	void delete_min(){
		curr_point--;
		swap(pac[0],pac[curr_point]);
		heapify(0);
		pac[curr_point]->reciever->recieved(pac[curr_point]);
	}
};







int main(){
	int n;
	cout<<"Number of nodes in the network"<<endl;
	cin>>n;
	Node* network[n];
	
	float trigger_time, curr_time=0;
	Packet_arrival next_arrival;
	Packet_dispatcher next_dispatch;


	for(int i = 0 ; i<n;i++){
		network[i] = new Node(i);
		cout<<"Network node: "<<network[i]->node_name()<<" initialised"<<endl;
	}	
	cout<<" Tell simul time"<<endl;
	cin>>trigger_time;

	for(int  i = 0 ; i< n;i++){
		int sent = rand()%n;
		float bytes = rand()%951 +50;
		if(i ==sent)sent++;
		sent%=n;
		next_arrival.insert(network[i]->send(bytes,0, network[sent]));
		next_dispatch.insert(network[i]);
		cout<<network[i]->node_name()<<endl;

	}
	while(curr_time < trigger_time){
		cout<<"Current time is "<< curr_time<<"s"<<endl;
		float nxt_arrival = next_arrival.min();
		float nxt_dispatch = next_dispatch.min();
		// cout<<endl<<endl<<nxt_dispatch<<" "<<nxt_arrival<<endl<<endl<<endl;
		if(nxt_dispatch > nxt_arrival){
			curr_time = nxt_arrival;
			if(curr_time > trigger_time)break;
			next_arrival.delete_min();
		}
		else {
			Node* nod = next_dispatch.delete_min();	
			curr_time = nxt_dispatch;
			if(curr_time > trigger_time)break;
			int sent = rand()%n;
			float bytes = rand()%951 +50;
			next_arrival.insert(nod->send(bytes , nxt_dispatch , network[sent]));
			next_dispatch.insert(nod);
		}
		cout<<"--------------------------------------"<<endl;
	}
}