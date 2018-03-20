import sys
from scipy.sparse import csr_matrix
import numpy as np
from Eval import Eval
from math import log, exp
from imdb import IMDBdata
import matplotlib.pyplot as plt

class NaiveBayes:
    def __init__(self, data, ALPHA=1.0):
        self.ALPHA = ALPHA
        self.data = data # training data
        #TODO: Initalize parameters
        self.vocab_len = data.vocab.GetVocabSize()
        # self.count_positive = 
        # self.count_negative = 
        # self.num_positive_reviews = 
        # self.num_negative_reviews = 
        # self.total_positive_words = 
        # self.total_negative_words = 
        # self.P_positive = 
        # self.P_negative = 
        # self.deno_pos = 
        # self.deno_neg =
        self.Train(data.X,data.Y)

    # Train model - X are instances, Y are labels (+1 or -1)
    # X and Y are sparse matrices
    def Train(self, X, Y):
        #TODO: Estimate Naive Bayes model parameters
        positive_indices = np.argwhere(Y == 1.0).flatten()
        negative_indices = np.argwhere(Y == -1.0).flatten()
        
        self.num_positive_reviews = len(positive_indices)
        self.num_negative_reviews = len(negative_indices)
        
        self.count_positive = np.ones([1,X.shape[1]]) * self.ALPHA 
        self.count_negative = np.ones([1,X.shape[1]]) * self.ALPHA 
        
        self.total_positive_words = 1 # initial 1 before
        self.total_negative_words = 1 # initial 1 before
        
        self.deno_pos = 1.0
        self.deno_neg = 1.0

        for index in range(X.shape[0]):
            if index in positive_indices:
                self.count_positive += X[index].toarray()
            elif index in negative_indices:
                self.count_negative += X[index].toarray()
        
        self.total_positive_words = np.sum(self.count_positive - self.ALPHA) 
        self.total_negative_words = np.sum(self.count_negative - self.ALPHA) 

        self.deno_pos = self.total_positive_words + self.vocab_len * self.ALPHA
        self.deno_neg = self.total_negative_words + self.vocab_len * self.ALPHA
        
        return

    # Predict labels for instances X
    # Return: Sparse matrix Y with predicted labels (+1 or -1)
    def PredictLabel(self, X):
        #TODO: Implement Naive Bayes Classification
#         self.P_positive = 1
#         self.P_negative = 1
        pred_labels = []
        self.P_positive = log(self.num_positive_reviews / (self.num_positive_reviews + self.num_negative_reviews))
        self.P_negative = log(self.num_negative_reviews / (self.num_positive_reviews + self.num_negative_reviews))
        logpos = np.array([[log(pos) for pos in (self.count_positive / self.deno_pos)[0]]])
        logneg = np.array([[log(neg) for neg in (self.count_negative / self.deno_neg)[0]]])
        sh = X.shape[0]
        for i in range(sh):
            self.P_positive += np.sum(logpos * X[i].toarray())
            self.P_negative += np.sum(logneg * X[i].toarray())

            if self.P_positive >= self.P_negative:  # Predict positive
                pred_labels.append(1.0)
            else:               # Predict negative
                pred_labels.append(-1.0)
            self.P_positive = log(self.num_positive_reviews / (self.num_positive_reviews + self.num_negative_reviews))
            self.P_negative = log(self.num_negative_reviews / (self.num_positive_reviews + self.num_negative_reviews))
        
        return pred_labels

    def LogSum(self, logx, logy):   
        # TO DO: Return log(x+y), avoiding numerical underflow/overflow.
        m = max(logx, logy)        
        return m + log(exp(logx - m) + exp(logy - m))

    # Predict the probability of each indexed review in sparse matrix text
    # of being positive
    # Prints results
    def PredictProb(self, test, indexes):
    
        for i in indexes:
            # TO DO: Predict the probability of the i_th review in test being positive review
            # TO DO: Use the LogSum function to avoid underflow/overflow
            predicted_label = 0
            log_prob_pos = np.sum(np.array([[log(pos) for pos in (self.count_positive / self.deno_pos)[0]]]) * test.X[i].toarray())
            log_prob_neg = np.sum(np.array([[log(neg) for neg in (self.count_negative / self.deno_neg)[0]]]) * test.X[i].toarray())
            logx = log_prob_pos + log(self.num_positive_reviews / (self.num_positive_reviews + self.num_negative_reviews))
            logy = log_prob_neg + log(self.num_negative_reviews / (self.num_positive_reviews + self.num_negative_reviews))
            deno = self.LogSum(logx,logy)

            predicted_prob_positive = exp(logx - deno)
            predicted_prob_negative = exp(logy - deno)
            
            if predicted_prob_positive > predicted_prob_negative:
                predicted_label = 1.0
            else:
                predicted_label = -1.0
            
            #print test.Y[i], test.X_reviews[i]
            # TO DO: Comment the line above, and uncomment the line below
            print(test.Y[i], predicted_label, predicted_prob_positive, predicted_prob_negative, test.X_reviews[i])

    def EvalPrecise(self, TP, FP):
        return TP / (TP + FP)

    def EvalRecall(self, TP, FN):
        return TP / (TP + FN)

    def PredictLabel_threshold(self, log_pos, log_neg, test, threshold = 0.5):
        TP = 0
        FP = 0
        FN = 0
        for i in range(test.X.shape[0]):
            predicted_label = 0
            log_prob_pos = np.sum(log_pos * test.X[i].toarray())
            log_prob_neg = np.sum(log_neg * test.X[i].toarray())
            logx = log_prob_pos + log(self.num_positive_reviews / (self.num_positive_reviews + self.num_negative_reviews))
            logy = log_prob_neg + log(self.num_negative_reviews / (self.num_positive_reviews + self.num_negative_reviews))
            deno = self.LogSum(logx,logy)            
            predict_posprob = exp(logx - deno)
            
            if predict_posprob > threshold:
                predicted_label = 1.0
            else:
                predicted_label = -1.0

            if predicted_label == 1.0 and test.Y[i] == 1.0:
                TP += 1
            elif predicted_label == -1.0 and test.Y[i] == 1.0:
                FP += 1
            elif predicted_label == 1.0 and test.Y[i] == -1.0:
                FN += 1

        return self.EvalPrecise(TP, FP), self.EvalRecall(TP, FN)

    def drawPreRec(self, test):
        thresholds = [x / 10 for x in range(1,10)]
        precise = []
        recall = []
        predict_posprob = []
        log_pos = np.array([[log(pos) for pos in (self.count_positive / self.deno_pos)[0]]])
        log_neg = np.array([[log(neg) for neg in (self.count_negative / self.deno_neg)[0]]])
        for threshold in thresholds:
            pre, rec = self.PredictLabel_threshold(log_pos, log_neg, test,threshold)
            precise.append(pre)
            recall.append(rec)
        plt.figure("Precise vs. Recall")
        plt.plot(thresholds,precise,'b-',label = 'precise')
        plt.plot(thresholds,recall,'r-',label = 'recall')
        plt.title('precise vs. recall')
        plt.legend(loc = 'upper left')
        plt.savefig('Precise_VS_Recall')

    # Evaluate performance on test data 
    def Eval(self, test):
        Y_pred = self.PredictLabel(test.X)
        ev = Eval(Y_pred, test.Y)
        return ev.Accuracy()

    def mostWords(self):
        pos_dict = {}
        neg_dict = {}
        pos_prob = self.count_positive / self.deno_pos
        neg_prob = self.count_negative / self.deno_neg
        for wid in range(pos_prob.shape[1]):
            pos_dict[self.data.vocab.GetWord(wid) + "_pos"] = pos_prob[0][wid]
            neg_dict[self.data.vocab.GetWord(wid) + "_neg"] = neg_prob[0][wid]

        return sorted(pos_dict.items(), key = lambda x : x[1], reverse = True)[:20], sorted(neg_dict.items(), key = lambda x : x[1], reverse = True)[:20]

if __name__ == "__main__":
    
    print("Reading Training Data")
    traindata = IMDBdata("%s/train" % sys.argv[1])
    print("Reading Test Data")
    testdata  = IMDBdata("%s/test" % sys.argv[1], vocab=traindata.vocab)    
    print("Computing Parameters")
    nb = NaiveBayes(traindata, float(sys.argv[2]))
    print("Evaluating")
    print("Test Accuracy: ", nb.Eval(testdata))
    nb = NaiveBayes(traindata, 1.0)
    indexes = [i for i in range(10)]
    print("First 10 reviews: ")
    nb.PredictProb(testdata, indexes)
    print("")
    nb.drawPreRec(testdata)
    pos_words, neg_words = nb.mostWords()
    str_pos = ""
    str_neg = ""
    for idx in range(len(pos_words)):
        str_pos += pos_words[idx][0] + " " + str(pos_words[idx][1]) + " "
        str_neg += neg_words[idx][0] + " " + str(neg_words[idx][1]) + " "
    print('20 Most positive words:')
    print(str_pos)
    print('20 Most negative words:')
    print(str_neg)