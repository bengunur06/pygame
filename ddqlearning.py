import tensorflow as tf
import numpy as np
import os
from dspcw import *

os.environ["SDL_VIDEODRIVER"] = "dummy" 

game = SpaceWarrior(84,84)
while game.run == True :
    
    game.reDrawGameWindow()




# Define Input Size
IMG_WIDTH = 84
IMG_HEIGHT = 84
NUM_STACK = 4
# For Epsilon-greedy
MIN_EXPLORING_RATE = 0.01

class Agent :
    def __init__(self,name,num_action,discount_factor=0.99):
        self.exploring_rate= 0.1
        self.discount_factor = discount_factor
        self.num_action = num_action
        self.model = self.build_model(name)

    def build_model(self,name):
        #input state
        #output each action's Q-value

        screen_stack = tf.keras.Input(shape=[IMG_WIDTH,IMG_HEIGHT,NUM_STACK],dtype=tf.float32)

        x = tf.keras.layers.Conv2D(filters=32,kernel_size=8,strides=4)(screen_stack)
        x = tf.keras.layers.ReLU()(x)
        x = tf.keras.layers.Conv2D(filters=64,kernel_size=4,strides=2)(x)
        x = tf.keras.layers.ReLU()(x)
        x = tf.keras.layers.Conv2D(filters=64,kernel_size=3,strides=1)(x)
        x = tf.keras.layers.ReLU()(x)
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(units=512)(x)
        x = tf.keras.layers.ReLU()(x)
        Q = tf.keras.layers.Dense(self.num_action)(x)

        model = tf.keras.Model(name=name,inputs = screen_stack,outputs=Q)

        return model 

    def loss(self,state,action,reward,tar_Q,terminal):
        # q(s,a,thetha) for all a ,  shape (batch_size,num_action )
        output = self.model(state)
        index = tf.stack([tf.range(tf.shape(action)[0]),action],axis=1)
        
        Q = tf.gather_nd(output,index)

        tar_Q =  ~np.array(terminal)
        loss = tf.reduce_mean(tf.square(reward + self.discount_factor * tar_Q -Q))

        return loss 

    def max_Q(self,state):

        output = self.model(state)

        return tf.reduce_max(output,axis=1)

    def select_action(self,state):

        if np.random.rand() < self.exploring_rate:
            action = np.random.choice(self.num_action)

        else :
            state = np.expand_dims(state,axis=0)
            output = self.model(state)
            action = tf.argmax(output,axis=1)[0]

        return action

    def update_parameters(self,episode):
        self.exploring_rate = max(MIN_EXPLORING_RATE,min(0.5,0.99**((episode)/ 30 )))

    def shutdown_explore(self):
        self.exploring_rate = 0


##init agent here

num_action = len(game.getActionSet())

##agent for frequently updating 
online_agent = Agent("online",num_action)

## agent for slow update 
target_agent = Agent("target",num_action)

target_agent.model.set_weights(online_agent.model.get_weights())

optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
average_loss = tf.keras.metrics.Mean(name="loss")

@tf.function 
def train_step(state,action,reward,next_state,terminal):
    tar_Q = target_agent.max_Q(next_state)
    with tf.GradientTape() as tape :
        loss = online_agent.loss(state,action,reward,tar_Q,terminal)
    gradients = tape.gradient(loss,online_agent.model.trainable.variables )
    optimizer.apply_gradients(zip(gradients,online_agent.model.trainable.variables))

    average_loss.update_state(loss)


class Replay_buffer():
    def __init__(self,buffer_size=50000):
        self.experiences = []
        self.buffer_size = buffer_size

    def add(self,experience):
        if len(self.experiences) > self.buffer_size:
            self.experiences.pop(0)
        self.experiences.append(experience)

    def sample(self,size):
        if size > len(self.experiences):
            experiences_idx = np.random.choice(len(self.experiences),size=size)
        else : 
            experiences_idx = np.random.choice(len(self.experiences),size=size,replace=False)


        states = []
        actions = []
        rewards = []
        states_prime = []
        terminal= []

        for i in range(size):
            states.append(self.experiences[experiences_idx[i][0]])
            actions.append(self.experiences[experiences_idx[i][1]])
            rewards.append(self.experiences[experiences_idx[i][2]])
            states_prime.append(self.experiences[experiences_idx[i][3]])
            terminal.append(self.experiences[experiences_idx[i][4]])

            return states, actions , rewards , states_prime , terminal

#init buffer 
buffer = Replay_buffer()

import moviepy.editor as mpy

def make_anim(images,fps = 60 , true_image = False):
    duration = len(images)/fps

    def make_frame(t):
        try :
            x = images[int(len(images)/duration * t )]
        except : 
            x = images[-1]

        if true_image:
            return x.astype(np.uint8)
        else : 
            return ((x+1) / 2 * 255 ).astype(np.uint8)
    
    clip = mpy.VideoClip(make_frame,duration=duration)
    clip.fps = fps 
    return clip

import skimage.transform as sti

def preprocess_screen(screen):
    screen = sti.resize(screen,[IMG_WIDTH,IMG_HEIGHT,1])
    return screen

def frames_to_state(input_frames):
    if(len(input_frames)==1):
        state = np.concatenate(input_frames*4,axis=-1)
    elif (len(input_frames)==2):
        state = np.concatenate(input_frames + input_frames[2:],axis=-1)
    elif (len(input_frames)==3):
        state = np.concatenate(input_frames + input_frames[2:],axis=-1)
    else : 
        state = np.concatenate(input_frames[-4:],axis=-1)

    return state

from IPython.display import Image,display





gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
    try:
        # Restrict TensorFlow to only use the fourth GPU
        #tf.config.experimental.set_visible_devices(gpus[3], 'GPU')

        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)