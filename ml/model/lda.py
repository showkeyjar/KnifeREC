# -*- coding: utf-8 -*-
import re
import codecs
import jieba
import pickle
import string
import warnings
import logging
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from gensim import corpora, models

"""
todo lda主题模型
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
stopwords = codecs.open('/data/rec/rec_lda/model/stop_words_cn.txt', 'r', encoding='utf8').readlines()
stopwords = [w.strip() for w in stopwords]
min_length = 100
train_set = []
doc_mapping = {}


def prepare_data(documents):
    global train_set, doc_mapping
    logging.debug('Start tokenzing the corpora')
    punct = re.compile('[%s]' % re.escape(string.punctuation))
    # doc_mapping = OrderedDict()

    def gen_train_set(patent):
        # print("send Series:" + str(patent))
        if 'name' in patent.keys():
            title = str(patent['name'])
            text = str(patent['desc'])
        else:
            text = ''
        # Skip document length < min_length
        if len(text) >= min_length:
            text = punct.sub("", text)  # Remove all punctuations
            tokens = jieba.cut(text)  # Tokenize the whole text
            # print(tokens)
            # Lemmatize every word and add to tokens list if the word is not in stopword
            train_set.append([word for word in tokens if word not in stopwords])
            # Build doc-mapping
            # k = str(patent['id']) if 'id' in patent.keys() is True else title
            doc_mapping[patent['id']] = title

    # tqdm.pandas(tqdm_notebook)
    documents.apply(gen_train_set, axis=1)
    logging.debug('Finished tokenzing the copora, train_set:' + str(len(train_set)))
    return len(train_set)


class LDAModel:
    def __init__(self, topic_num=900, min_doc=50, iter_num=100, pass_num=100):
        # Built-in dictionary for word-parser, and path to corpora
        self.stopword = stopwords
        warnings.filterwarnings("ignore")

        # Hyperparameters for training model
        # Minimun length of single document
        self.min_length = min_doc
        # Num_topics in LDA
        self.num_topics = topic_num
        # Filter out tokens that appear in less than `no_below` documents (absolute number)
        self.no_below_this_number = 5
        # Filter out tokens that appear in more than `no_above` documents (fraction of total corpus size, *not* absolute number).
        self.no_above_fraction_of_doc = 0.33
        # Remove topic which weights less than this number
        self.remove_topic_so_less = 0.05
        # Number of iterations in training LDA model, the less the documents in total, the more the iterations for LDA model to converge
        self.num_of_iterations = iter_num
        # Number of passes in the model
        self.passes = pass_num
        # Print all hyperparameters
        parameters = {}
        parameters['min_length'] = self.min_length
        parameters['num_topics'] = self.num_topics
        parameters['no_below_this_number'] = self.no_below_this_number
        parameters['no_above_fraction_of_doc'] = self.no_above_fraction_of_doc
        parameters['remove_topic_so_less'] = self.remove_topic_so_less
        parameters['num_of_iterations'] = self.num_of_iterations
        parameters['passes'] = self.passes
        for k in parameters:
            logging.debug("Parameter for {0} is {1}".format(k, parameters[k]))
        logging.debug('Finished initializing....')

    def __convertListToDict(self, anylist):
        '''
        This code snippet could be easily done by one-liner dict comprehension:
        {key:value for key,value in anylist}
        '''
        convertedDict = {}
        for pair in anylist:
            topic = pair[0]
            weight = pair[1]
            convertedDict[topic] = weight
        return convertedDict

    def __savePickleFile(self, fileName, objectName):
        '''
        Serialize objects into pickle files
        '''
        fileName = '/data/rec/rec_lda/model/' + fileName + '.pickle'
        mappingFile = open(fileName, 'wb')
        pickle.dump(objectName, mappingFile)
        mappingFile.close()

    def saveModel(self, lda, doc_mapping, dic, corpus, tail=''):
        '''
        Saving models and maps for later use
        :param lda: the LDA model
        :param doc_mapping: index-document mapping
        :param corpus: the whole corpus in list[list[tokens]]
        :param tail:
        '''
        logging.debug('Start saving LDA models & maps....')
        # Save model output
        save_path = '/data/rec/rec_lda/model/final_ldamodel' + tail
        lda.save(save_path)
        logging.debug('Model saved at {0}'.format(save_path))
        # Save dict
        save_path = '/data/rec/rec_lda/model/dic.dict' + tail
        dic.save(save_path)
        # Save the whole corpus
        save_path = 'corpus' + tail
        self.__savePickleFile(save_path, corpus)
        logging.debug('Corpus saved at {0}'.format(save_path))
        # Save index to document mapping
        save_path = 'documentmapping' + tail
        self.__savePickleFile(save_path, doc_mapping)
        logging.debug('Document mapping saved at {0}'.format(save_path))
        # Save index to link mapping
        # save_path = 'linkmapping'
        # self.__savePickleFile(save_path, link_mapping)
        # print('Link mapping saved at {0}'.format(save_path))
        # Save doc to topic matrix
        doc_topic_matrix = {}
        logging.debug('CORPUS: {}'.format(len(corpus)))

        for index, p_id in enumerate(doc_mapping.keys()):
            dense_vector = {}
            vector = self.__convertListToDict(lda[corpus[index]])
            # remove topic that is so irrelevant
            for topic in vector:
                if vector[topic] > self.remove_topic_so_less:
                    dense_vector[topic] = vector[topic]
            doc_topic_matrix[p_id] = dense_vector

        save_path = 'doc_topic_matrix' + tail
        self.__savePickleFile(save_path, doc_topic_matrix)
        logging.debug('doc to topic mapping saved at {0}'.format(save_path))
        logging.debug('Finished saving LDA models & maps....')

    def trainModel(self, debug=False):
        '''
        Train a LDA model, inclusive of 4 steps:
        1. Parse the whole corpora into unigram token collections and document mapping (for later use)
        2. Filter tokens which are not common (no_below_this_number), and too common (no_above_fraction_of_doc)
        3. Indexing the token collections and do TF-IDF transformation
        4. Call gensim.models.LdaModel and generate topic distributions of the corpora
        '''
        global train_set, doc_mapping
        logging.debug('Start preparing unigram tokens....')
        # Start of preparing list of documents and tokens [[words_in_1st_doc],[words_in_2nd_doc]....], which comprise Bag-Of-Words (BOW)
        # Get document_count, tokens, and document-index mapping from the corpora

        # Put the training data into gensim.corpora for later use
        dic = corpora.Dictionary(train_set)
        denominator = len(dic)
        # Filtering infrequent words & common stopwords, thus reducing the dimension of terms (which prevents curse of dimensionality)
        dic.filter_extremes(no_below=self.no_below_this_number, no_above=self.no_above_fraction_of_doc)
        nominator = len(dic)
        corpus = [dic.doc2bow(text) for text in train_set]  # transform every token into BOW
        if debug:
            # print('There are {} documents in the pool'.format(len(documents)))
            logging.debug("In the corpus there are " + str(denominator) + " raw tokens")
            if denominator > 0:
                logging.debug("After filtering, in the corpus there are " + str(nominator) + " unique tokens, reduced " + str(
                    1 - (nominator / denominator)) + "%")
            logging.debug('Finished preparing unigram tokens....')
        # END
        logger.debug('Start training LDA model....')
        # Implementing TF-IDF as a vector for each document, and train LDA model on top of that
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        logger.debug('use TF-IDF filter corpus.')
        # 设置 eval_every=1 每次迭代均计算困惑度
        lda = models.LdaModel(corpus_tfidf, id2word=dic, num_topics=self.num_topics, eval_every=1,
                              iterations=self.num_of_iterations, passes=self.passes)
        corpus_lda = lda[corpus_tfidf]
        # 直接应用 lda
        # lda = models.LdaModel(corpus, id2word=dic, num_topics=self.num_topics, iterations=self.num_of_iterations, passes=self.passes)
        # corpus_lda = lda[corpus]
        # Once done training, print all the topics and related words
        if debug:
            logging.debug('Finished training LDA model.......Here is the list of all topics & their most frequent words')
            for i in range(self.num_topics):
                logging.debug('Topic {} : {}'.format(str(i), lda.print_topic(i)))
            # Exhibit perplexity of current model under specific topic hyperparameter : k. The lower the better
            logging.debug('===============================')
        perplexity = lda.bound(corpus_lda)
        logging.debug('Model perplexity : ' + str(perplexity) + ' when topic k = ' + str(self.num_topics))
        return lda, doc_mapping, dic, corpus_tfidf, perplexity


class Predict():
    def __init__(self, tail=''):
        # current_working_dir = '/data/rec/rec_lda/'
        # os.chdir(current_working_dir)
        lda_model_path = "/data/rec/rec_lda/model/final_ldamodel" + tail
        self.tail = tail
        self.lda = LdaModel.load(lda_model_path)
        self.dic = Dictionary.load('/data/rec/rec_lda/model/dic.dict' + tail)
        self.corpus = loadPickleFile('corpus' + tail)
        self.max_token_index = self.__get_max_token_index()
        self.no_of_recommendation = 10
        self.omit_topic_below_this_fraction = 0.1
        self.mapping = self.__init_mapping()
        self.doc_topic_matrix = loadPickleFile('doc_topic_matrix' + tail)

    def __init_mapping(self):
        path_mappingfile = '/data/rec/rec_lda/model/documentmapping' + self.tail + '.pickle'
        mappingFile = open(path_mappingfile, 'rb')
        mapping = pickle.load(mappingFile)
        mappingFile.close()
        return mapping

    def __get_max_token_index(self):
        token_index = 0
        for doc in self.corpus:
            for pair in doc:
                if int(pair[0]) > token_index:
                    token_index = int(pair[0])
        return token_index

    def constructDocToTopicMatrix(self, lda, corpus):
        '''
        This code snippet could be easily done by one-liner dict comprehension:
        {key:value for key,value in anylist}
        '''
        doc_topic_matrix = {}
        count = 0
        for doc in corpus:
            if len(doc) > 0:
                count = count + 1
                vector = convertListToDict(lda[doc])
                doc_topic_matrix[count] = vector
        return doc_topic_matrix

    def constructDocDictToTopicMatrix(self, weight_dict, verbose=False):
        user_topic_vector = {}
        length = len(weight_dict)
        try:
            for seen_topic, weight in weight_dict.items():
                # weight = user_dict[seen_doc][seen_topic]
                if seen_topic in user_topic_vector:
                    current_weight = user_topic_vector[seen_topic]
                    current_weight = current_weight + weight / length
                    user_topic_vector[seen_topic] = current_weight
                else:
                    user_topic_vector[seen_topic] = weight / length
        except Exception as e:
            logger.debug(e)
            logger.debug('Warning: wrong value of weight_dict:' + str(weight_dict))
        lightweight_user_topic_vector = {}
        for k, v in user_topic_vector.items():
            if v > self.omit_topic_below_this_fraction / 2:
                lightweight_user_topic_vector[k] = v

        denominator = sum(lightweight_user_topic_vector.values())

        for topic in lightweight_user_topic_vector:
            lightweight_user_topic_vector[topic] = lightweight_user_topic_vector[topic] / denominator

        if verbose:
            logger.debug('Topic distribution for current user : {0}'.format(lightweight_user_topic_vector))
            logger.debug('Normalized topic distribution for current user : {0}'.format(lightweight_user_topic_vector))

        return lightweight_user_topic_vector

    def constructUserToTopicMatrix(self, user_dict, verbose=False):
        """ Construct user-topic vector(dictionary)
        args:
            user_dict: a dictionary of user-doc and doc-topic
        """
        user_topic_vector = {}
        length = len(user_dict)
        for seen_doc, seen_topics in user_dict.items():
            try:
                for seen_topic, weight in seen_topics.items():
                    # weight = user_dict[seen_doc][seen_topic]
                    if seen_topic in user_topic_vector:
                        current_weight = user_topic_vector[seen_topic]
                        current_weight = current_weight + weight / length
                        user_topic_vector[seen_topic] = current_weight
                    else:
                        user_topic_vector[seen_topic] = weight / length
            except Exception as e:
                logger.debug(e)
                logger.debug('Warning: wrong value of seen_topics:' + str(seen_topics))
        # Remove topic less than weight : omit_topic_below_this_fraction/2
        lightweight_user_topic_vector = {}
        for k, v in user_topic_vector.items():
            if v > self.omit_topic_below_this_fraction / 2:
                lightweight_user_topic_vector[k] = v

        denominator = sum(lightweight_user_topic_vector.values())

        for topic in lightweight_user_topic_vector:
            lightweight_user_topic_vector[topic] = lightweight_user_topic_vector[topic] / denominator

        if verbose:
            logger.debug('Topic distribution for current user : {0}'.format(lightweight_user_topic_vector))
            logger.debug('Normalized topic distribution for current user : {0}'.format(lightweight_user_topic_vector))

        return lightweight_user_topic_vector

    def getLink(self, sort, no_of_recommendation):
        for i in list(sort.keys())[:no_of_recommendation]:
            logger.debug('Recommend document: {0} '.format(self.mapping[i]))

    def gen_corpus(self, doc_text):
        tokens = jieba.cut(doc_text)
        # user_corpus = [self.dic.doc2bow(text) for text in [tokens]]
        user_corpus = []
        for text in [tokens]:
            try:
                bow = self.dic.doc2bow(text)
            except Exception as e:
                logger.warning(e)
                try:
                    bow = self.dic.doc2bow(list(text))
                except:
                    bow = None
                # logger.debug('Warning: doc2bow error for text:' + str(text))
            if bow is not None:
                user_corpus.append(bow)
        ret_corpus = None
        if len(user_corpus) > 0:
            ret_corpus = user_corpus[0]
        return ret_corpus

    def gen_doc_matrix(self, text):
        text_corpus = self.gen_corpus(text)
        lightweight_user_topic_vector = {}
        if text_corpus is not None:
            # 删除语料库中未出现的关键词
            t_key = []
            for pair in text_corpus:
                token_index = int(pair[0])
                # logger.debug(token_index)
                if token_index <= self.max_token_index:
                    t_key.append(pair)
            text_score = self.lda[t_key]
            text_dict = convertListToDict(text_score)
            user_topic_vector = {}
            for seen_topic in text_dict:
                weight = text_dict[seen_topic]
                if seen_topic in user_topic_vector:
                    current_weight = user_topic_vector[seen_topic]
                    current_weight = current_weight + weight
                    user_topic_vector[seen_topic] = current_weight
                else:
                    user_topic_vector[seen_topic] = weight
            for k, v in user_topic_vector.items():
                if v > 0.05:
                    lightweight_user_topic_vector[k] = v
            denominator = sum(lightweight_user_topic_vector.values())
            for topic in lightweight_user_topic_vector:
                lightweight_user_topic_vector[topic] = lightweight_user_topic_vector[topic] / denominator
        return lightweight_user_topic_vector

    def predict_matrix(self, user_matrix, prob=0.7):
        recommend_dict = {}
        # Pearson correlation appears to be the most precise 'distance' metric in this case
        for doc in self.doc_topic_matrix:
            # sim = cossim(user_topic_matrix, self.doc_topic_matrix[doc])  # cosine similarity
            # sim = KLDivergenceSim(user_topic_matrix, self.doc_topic_matrix[doc], self.lda.num_topics)  # KLD similarity
            sim = pearson_correlation(user_matrix, self.doc_topic_matrix[doc], self.lda.num_topics)
            if sim > prob:  # 0.7 is arbitrary, subject to developer's judge
                recommend_dict[doc] = sim
        # sort the dict descending by similarity
        sort = getOrderedDict(recommend_dict)
        return sort

    def predict_text(self, text, prob=0.7):
        lightweight_user_topic_vector = self.gen_doc_matrix(text)
        sort = self.predict_matrix(lightweight_user_topic_vector, prob)
        return sort

    def predict_doc(self, doc_dict, verbose=False, prob=0.7):
        logger.debug('Doc dict: {}'.format(doc_dict))
        one_doc_topic_matrix = self.constructDocDictToTopicMatrix(doc_dict, verbose)
        recommend_dict = {}
        # Pearson correlation appears to be the most precise 'distance' metric in this case
        for doc in self.doc_topic_matrix:
            # sim = cossim(user_topic_matrix, self.doc_topic_matrix[doc])  # cosine similarity
            # sim = KLDivergenceSim(user_topic_matrix, self.doc_topic_matrix[doc], self.lda.num_topics)  # KLD similarity
            sim = pearson_correlation(one_doc_topic_matrix, self.doc_topic_matrix[doc], self.lda.num_topics)
            if sim > prob and doc not in doc_dict.keys():  # 0.7 is arbitrary, subject to developer's judge
                if verbose:
                    logger.debug('Recommend document {0} of similarity : {1}'.format(doc, sim))
                recommend_dict[doc] = sim
        # sort the dict descending by similarity
        sort = getOrderedDict(recommend_dict)
        #recommend_str = str(list(sort.keys())[:self.no_of_recommendation]).replace('[', '').replace(']', '')
        if verbose:
            for title in doc_dict:
                logger.debug('You viewed : {0}'.format(self.mapping[title]))
            self.getLink(sort, self.no_of_recommendation)
        return sort

    def predict(self, user_dict, verbose=False, prob=0.7):
        '''
        Get recommendations from the user_dict which describes the topic distribution attibutes to a user/item
        If verbose = True, return the result in a verbose way.
        '''
        logger.debug('User dict: {}'.format(user_dict))
        user_topic_matrix = self.constructUserToTopicMatrix(user_dict, verbose)
        recommend_dict = {}
        # Pearson correlation appears to be the most precise 'distance' metric in this case
        for doc in self.doc_topic_matrix:
            # sim = cossim(user_topic_matrix, self.doc_topic_matrix[doc])  # cosine similarity
            # sim = KLDivergenceSim(user_topic_matrix, self.doc_topic_matrix[doc], self.lda.num_topics)  # KLD similarity
            sim = pearson_correlation(user_topic_matrix, self.doc_topic_matrix[doc], self.lda.num_topics)
            if sim > prob and doc not in user_dict.keys():  # 0.7 is arbitrary, subject to developer's judge
                if verbose:
                    logger.debug('Recommend document {0} of similarity : {1}'.format(doc, sim))
                recommend_dict[doc] = sim
        # sort the dict descending by similarity
        sort = getOrderedDict(recommend_dict)
        #recommend_str = str(list(sort.keys())[:self.no_of_recommendation]).replace('[', '').replace(']', '')
        if verbose:
            for title in user_dict:
                logger.debug('You viewed : {0}'.format(self.mapping[title]))
            self.getLink(sort, self.no_of_recommendation)
        return sort



if __name__ == '__main__':
    parser = ArgumentParser(description="LDAModel", formatter_class=RawDescriptionHelpFormatter)
    # parser.add_argument("-i", "--index", default=True, help="Mapping by index")
    parser.add_argument("-d", "--doc", default=True, help="Target documents")
    # doc is pd.DataFrame, construct:
    # id	name	desc
    args = parser.parse_args()
    prepare_data(args.doc)
    LDAmodel = LDAModel()  # instantiate the LDAModel class
    lda, doc_mapping, corpus = LDAmodel.trainModel()  # train a LDA model using the assgined corpora
    LDAmodel.saveModel(lda, doc_mapping, corpus)  # save model for recommendations use
