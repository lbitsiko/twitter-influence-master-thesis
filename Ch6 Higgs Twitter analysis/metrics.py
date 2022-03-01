def general_selection_for_metrics(df, node_i, label1, label2):
    return df.where(df[label1] == node_i).dropna()[label2]


def f1_metric(graph):
    """
        F1: Number of followers.
    """
    return dict(graph.in_degree)


def f3_metric(graph):
    """
        F3: Number of followees.
    """
    return dict(graph.out_degree)

def all_metrics(graph, df_mention, df_reply, df_retweet):
    return_dict = {
        'f1': f1_metric(graph),
        'f3': f3_metric(graph),
        'm1': {},
        'm2': {},
        'm3': {},
        'm4': {},
        'rt1': {},
        'rt2': {},
        'rt3': {},
        'rp1': {},
        'rp3': {}
    }
    for i in graph.nodes():
        return_dict['m1'][i] = 0.0
        return_dict['m2'][i] = 0.0
        return_dict['m3'][i] = 0.0
        return_dict['m4'][i] = 0.0
        return_dict['rt1'][i] = 0.0
        return_dict['rt2'][i] = 0.0
        return_dict['rt3'][i] = 0.0
        return_dict['rp1'][i] = 0.0
        return_dict['rp3'][i] = 0.0

    for _, row in df_mention.iterrows():
        if row.A in return_dict['m1'].keys():
            return_dict['m1'][row.A] += row.w
        if row.A in return_dict['m2'].keys():
            return_dict['m2'][row.A] += 1.0
        if row.B in return_dict['m3'].keys():
            return_dict['m3'][row.B] += row.w
        if row.B in return_dict['m4'].keys():
            return_dict['m4'][row.B] += 1.0

    for _, row in df_retweet.iterrows():
        if row.A in return_dict['rt1'].keys():
            return_dict['rt1'][row.A] += row.w
        if row.B in return_dict['rt2'].keys():
            return_dict['rt2'][row.B] += row.w
        if row.B in return_dict['rt3'].keys():
            return_dict['rt3'][row.B] += 1.0

    for _, row in df_reply.iterrows():
        if row.A in return_dict['rp1'].keys():
            return_dict['rp1'][row.A] += row.w
        if row.B in return_dict['rp3'].keys():
            return_dict['rp3'][row.B] += 1.0
    return return_dict


# def all_metrics_inefficient(graph, df_mention, df_reply, df_retweet):
#     return_dict = {
#         'f1': dict(f1_metric(graph)),
#         'f3': dict(f3_metric(graph)),
#         'm1': {},
#         'm2': {},
#         'm3': {},
#         'm4': {},
#         'rt1': {},
#         'rt2': {},
#         'rt3': {},
#         'rp1': {},
#         'rp3': {}
#     }
#     for i in graph.nodes():
#         return_dict['m1'][i] = general_selection_for_metrics(df_mention, i, 'A', 'w').sum()
#         return_dict['m2'][i] = len(set(general_selection_for_metrics(df_mention, i, 'A', 'B')))
#         return_dict['m3'][i] = general_selection_for_metrics(df_mention, i, 'B', 'w').sum()
#         return_dict['m4'][i] = len(set(general_selection_for_metrics(df_mention, i, 'B', 'A')))
#         return_dict['rt1'][i] = general_selection_for_metrics(df_retweet, i, 'A', 'w').sum()
#         return_dict['rt2'][i] = general_selection_for_metrics(df_retweet, i, 'B', 'w').sum()
#         return_dict['rt3'][i] = len(set(general_selection_for_metrics(df_retweet, i, 'B', 'A')))
#         return_dict['rp1'][i] = general_selection_for_metrics(df_reply, i, 'A', 'w').sum()
#         return_dict['rp3'][i] = len(set(general_selection_for_metrics(df_reply, i, 'B', 'A')))
#     return return_dict
#
#
# def m1_rp1_rt1_metric_inefficient(graph, df):
#     # M1: Number of mentions to other users by the author.
#     # RP1: Number of replies posted by the author.
#     # RT1: Number of retweets accomplished by the author.
#     return_dict = {}
#     for i in graph.nodes:
#         return_dict[i] = general_selection_for_metrics(df, i, 'A', 'w').sum()
#     return return_dict
#
#
# def m3_rt2_metric_inefficient(graph, df):
#     # M3: Number of mentions to the author by other users
#     # RT2: Number of OTs posted by the author and retweeted by other users.
#     return_dict = {}
#     for i in graph.nodes:
#         return_dict[i] = general_selection_for_metrics(df, i, 'B', 'w').sum()
#     return return_dict
#
#
# def m2_metric_inefficient(graph, df):
#     # M2: Number of users mentioned by the author.
#     return_dict = {}
#     for i in graph.nodes:
#         return_dict[i] = len(set(general_selection_for_metrics(df, i, 'A', 'B')))
#     return return_dict
#
#
# def m4_rp3_rt3_metric_inefficient(graph, df):
#     # M4: Number of users mentioning the author
#     # RP3: Number of users who have replied author’s tweets.
#     # RT3: Number of users who have retweeted author’s tweets.
#     return_dict = {}
#     for i in graph.nodes:
#         return_dict[i] = len(set(general_selection_for_metrics(df, i, 'B', 'A')))
#     return return_dict


def m1_metric(graph_social, df_mention):
    """
        M1: Number of mentions to other users by the author.
    """
    m1_dict = {}
    for i in graph_social.nodes:
        m1_dict[i] = 0.0
    for _, row in df_mention.iterrows():
        # if row.A in m1_dict.keys():
        #     m1_dict[row.A] += row.w
        try:
            m1_dict[row.A] += row.w
        except KeyError:
            pass
    return m1_dict


def m2_metric(graph_social, df_mention):
    """
        M2: Number of users mentioned by the author.
    """
    m2_dict = {}
    for i in graph_social.nodes:
        m2_dict[i] = 0.0
    for _, row in df_mention.iterrows():
        # if row.A in m2_dict.keys():
        #     m2_dict[row.A] += 1.0
        try:
            m2_dict[row.A] += 1.0
        except KeyError:
            pass
    return m2_dict


def m3_metric(graph_social, df_mention):
    """
        M3: Number of mentions to the author by other users.
    """
    m3_dict = {}
    for i in graph_social.nodes:
        m3_dict[i] = 0.0
    for _, row in df_mention.iterrows():
        try:
            m3_dict[row.B] += row.w
        except KeyError:
            pass
        # if row.B in m3_dict.keys():
        #     m3_dict[row.B] += 1.0
    return m3_dict

def m4_metric(graph_social, df_mention):
    """
        M4: Number of users mentioning the author
    """
    m4_dict = {}
    for i in graph_social.nodes:
        m4_dict[i] = 0.0
    for _, row in df_mention.iterrows():
        try:
            m4_dict[row.B] += 1.0
        except KeyError:
            pass
    return m4_dict


# def m1_metric_inefficient(graph_social, df_mention):
#     m1_dict = {}  # Number of mentions to other users by the author.
#     for i in graph_social.nodes:
#         mentions_by_i_to_other_users = df_mention.where(df_mention.A == i).dropna()
#         m1_dict[i] = mentions_by_i_to_other_users.w.sum()
#     return m1_dict
#
#
# def m2_metric_inefficient(graph_social, df_mention):
#     m2_dict = {}
#     for i in graph_social.nodes:
#         mentions_by_i_to_other_users = df_mention.where(df_mention.A == i).dropna()
#         users_i_mentioned = set(mentions_by_i_to_other_users.B)
#         m2_dict[i] = len(users_i_mentioned)
#     return m2_dict
#
#
# def m3_metric_inefficient(graph_social, df_mention):
#     m3_dict = {}  # Number of mentions to the author by other users
#     for i in graph_social.nodes:
#         mentions_to_i_by_others = df_mention.where(df_mention.B == i).dropna()
#         m3_dict[i] = mentions_to_i_by_others.w.sum()
#     return m3_dict
#
# def m4_metric_inefficient(graph_social, df_mention):
#     m4_dict = {}  # Number of users mentioning the author
#     for i in graph_social.nodes:
#         mentions_to_i_by_others = df_mention.where(df_mention.B == i).dropna()
#         users_mentioning_i = set(mentions_to_i_by_others.A)
#         m4_dict[i] = len(users_mentioning_i)
#     return m4_dict
#
#
# def m_metrics_inefficient(graph_social, df_mention):
#     m1_dict = {}  # Number of mentions to other users by the author.
#     m2_dict = {}  # Number of users mentioned by the author.
#     m3_dict = {}  # Number of mentions to the author by other users
#     m4_dict = {}  # Number of users mentioning the author
#     for i in graph_social.nodes:
#         mentions_by_i_to_other_users = df_mention.where(df_mention.A == i).dropna()
#         users_i_mentioned = set(mentions_by_i_to_other_users.B)
#         mentions_to_i_by_others = df_mention.where(df_mention.B == i).dropna()
#         users_mentioning_i = set(mentions_to_i_by_others.A)
#
#         m1_dict[i] = mentions_by_i_to_other_users.w.sum()
#         m2_dict[i] = len(users_i_mentioned)
#
#         m3_dict[i] = mentions_to_i_by_others.w.sum()
#         m4_dict[i] = len(users_mentioning_i)
#
#     return m1_dict, m2_dict, m3_dict, m4_dict


def rp1_metric(graph_social, df_reply):
    """"
        RP1: Number of replies posted by the author.
    """
    rp1_dict = {}
    for i in graph_social.nodes:
        rp1_dict[i] = 0.0
    for _, row in df_reply.iterrows():
        try:
            rp1_dict[row.A] += row.w
        except KeyError:
            pass
    return rp1_dict


def rp3_metric(graph_social, df_reply):
    """
        RP3: Number of users who have replied author’s tweets.
    """
    rp3_dict = {}
    for i in graph_social.nodes:
        rp3_dict[i] = 0.0
    for _, row in df_reply.iterrows():
        try:
            rp3_dict[row.B] += 1.0
        except KeyError:
            pass
    return rp3_dict

def rt1_metric(graph_social, df_retweet):
    """
        RT1: Number of retweets accomplished by the author.
    """
    rt1_dict = {}
    for i in graph_social.nodes:
        rt1_dict[i] = 0.0
    for _, row in df_retweet.iterrows():
        try:
            rt1_dict[row.A] += row.w
        except KeyError:
            pass
    return rt1_dict


def rt2_metric(graph_social, df_retweet):
    """
        RT2: Number of OTs posted by the author and retweeted by other users.
    """
    rt2_dict = {}
    for i in graph_social.nodes:
        rt2_dict[i] = 0.0
    for _, row in df_retweet.iterrows():
        try:
            rt2_dict[row.B] += row.w
        except KeyError:
            pass
    return rt2_dict


def rt3_metric(graph_social, df_retweet):
    """
        RT3: Number of users who have retweeted author’s tweets.
    """
    rt3_dict = {}
    for i in graph_social.nodes:
        rt3_dict[i] = 0.0
    for _, row in df_retweet.iterrows():
        try:
            rt3_dict[row.B] += 1.0
        except KeyError:
            pass
    return rt3_dict


# def rp1_metric_inefficient(graph_social, df_reply):
#     rp1_dict = {}  # Number of replies posted by the author.
#     for i in graph_social.nodes:
#         replies_by_i_to_other_users = df_reply.where(df_reply.A == i).dropna()
#         rp1_dict[i] = replies_by_i_to_other_users.w.sum()
#     return rp1_dict
#
#
# def rp3_metric_inefficient(graph_social, df_reply):
#     rp3_dict = {}  # Number of users who have replied author’s tweets.
#     for i in graph_social.nodes:
#         replies_to_i_by_others = df_reply.where(df_reply.B == i).dropna()
#         users_replying_to_i = set(replies_to_i_by_others.A)
#         rp3_dict[i] = len(users_replying_to_i)
#     return rp3_dict
#
#
# def rt1_metric_inefficient(graph_social, df_retweet):
#     rt1_dict = {}  # Number of retweets accomplished by the author.
#     for i in graph_social.nodes:
#         retweets_posted_by_i = df_retweet.where(df_retweet.A == i).dropna()
#         rt1_dict[i] = retweets_posted_by_i.w.sum()
#     return rt1_dict
#
#
# def rt2_metric_inefficient(graph_social, df_retweet):
#     rt2_dict = {}  # Number of OTs posted by the author and retweeted by other users.
#     for i in graph_social.nodes:
#         retweets_of_posts_of_i_by_others = df_retweet.where(df_retweet.B == i).dropna()
#         rt2_dict[i] = retweets_of_posts_of_i_by_others.w.sum()
#     return rt2_dict
#
#
# def rt3_metric_inefficient(graph_social, df_retweet):
#     rt3_dict = {}  # Number of users who have retweeted author’s tweets.
#     for i in graph_social.nodes:
#         users_who_have_retweeted_posts_of_i = set(df_retweet.where(df_retweet.B == i).dropna().A)
#         rt3_dict[i] = len(users_who_have_retweeted_posts_of_i)
#     return rt3_dict
