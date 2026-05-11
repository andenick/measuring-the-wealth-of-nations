# Chapter 11: Recasting Input-Output Networks in a Marxist Framework
## Pages 239-248 (Book pages 261-270 in chunk)

---

## Page 239

acting as hubs propagate individual sectoral shocks through the whole networks without a decay.

Lorenzo Burlon (2011) ingeniously mixes the arguments of Gabaix and Carvalho and underlines the argument that the propagation mechanism depends both on the firm and sector level interdependencies. The first derives from the nature of conglomerates of firms and establishments. Each establishment operates in one sector but produces externalities for other conglomerate establishments operating in other sectors. The second interdependency derives from the substitutability/complementarity of sectors.

Fisher and Vega-Redondo (2006) claim to be the first study in which centrality measures in cross country I-O networks are calculated. The originality of measures derives from weighted and directed characteristics of the edges. They find that there are a few central sectors across 20 countries' I-O networks, such as Wholesale and Retail Trade, Finance, Business Services, and a couple of manufacturing sectors (motor vehicles or machinery). They also underline the fact that Real Estate ranks first in terms of the Counting Betweenness measure in 2003 for US I-O network. Its measure (107.5) is as big as almost twice the Administrative and Support Services (57.8). Retrospectively, we think this is very important as it reflects the real estate bubble building in the United States till 2008.

Blöchl et al. (2011) propose two new measures for sector centralities in national input-output networks and demonstrate that these measures relate to the development status of the national economies. We follow and extend their analysis in reconstructing the input-output networks of the United States, Germany, and Spain a la Marxian framework.

## Section 3: Input-Output Networks and the Counting Betweenness Centrality Measure

The intermediate input flows in an I-O table can be considered as a network in which the sectors are the vertices, and the input flows designate the directed and weighted edges. These networks can be formulated in terms of adjacency matrices of which the cells F_ij signify the input flows from sector i into sector j. The intermediate input flows network reflects only the transactions among firms (aggregated into a sector) that cover the sales of goods and services that are directly used up as inputs in the production processes. The underlying system is not closed as the

---

## Page 240

sum of rows and columns do not match. In national accounts, the total value of the gross output of a sector also includes sales for final demand, i.e. consumption, investment, government purchases and net exports. The total value of gross inputs into a sector also includes payments to the factors of production, i.e. gross operating surplus, compensation to employees and indirect business taxes.

About 10-15% of the cells are zero, meaning that there are no interactions in terms of input flows among these sectors. There are various levels of self-loops; for example, in the US 2005 I-O network about 64% of all intermediate inputs originating from the "Motor Vehicles" sector is used up by the same sector.

The database we employ comes from the OECD Stan Input-Output Tables. The industry classification of the database is based on the ISIC Rev. 3 system. Unfortunately, information on all 48 industrial sectors could not be obtained for every country. We use the highest number of available sectors for each country.

We will follow a new method in estimating the Counting Betweenness centrality measures of the sectors in the I-O networks. Although there are older and more conventional measures of centrality depending on basic network characteristics, we prefer the new measure. Conventional centrality measures based on shortest-path or betweenness are inadequate in our context for mainly three reasons.

1. The input-output networks are nearly complete; thus, the shortest-path does not really make sense.
2. These networks are directed and weighted.
3. The self-loops are important, and the conventional measures do not take this feature into account.

The new measure "Counting Betweenness centrality" (CB in short) is based on the random walk concept. Flows of intermediate goods from one sector to another and flows of "money" back from the latter to the former constitute the main interdependencies among sectors. Had we

---

## Page 241

been trying to find out which sectors would be most important in terms of their effects on the aggregate output, the conventional input-output measures of forward and backward linkages could have been appropriate. However, we are rather interested in picking the most vulnerable sectors in an economy in which each and every sector can face a supply or demand shock with an equal (and random) probability.

Random walks specify origin and target sectors. Flows of intermediate goods and money (in return) leave the system once they reach the target sector through direct and indirect walks. The probability of a certain walk depends on the edge weights, that is, the value of the out-degrees.

In a random walk, flows will follow a probability distribution in passing from one vertex to another. The probability distribution in turn depends on the relative weight of the edges connecting the vertices.

First, out-strength of each sector is calculated as k_i = Σ_{j=1} a_ij. Then the whole matrix is normalised, and the transition matrix is obtained, M = K^{-1}A, where A denotes the adjacency matrix and K is the diagonal of the out-strength matrix.

For a random walk between a source vertex s and a target vertex t, t ≠ s, the probability of completion of the walk in r steps is ((M_{-t})^r)_{si}. By the target sector we mean the sector in which the flows end up as an extra output which satisfies the final consumption demand, and hence leaves the system.

Then the probability of a path from i to j being completed (could be in any number of steps) is m_ij. If we add all the different possibilities of random walks that pass a given edge, we get

N^{st}_{ij} = Σ_r ((M_{-t})^r)_{si} m_{ij} = m_{ij}((I^{-1} - M_{-t})^{-1})_{si}

Since any vertex i can be visited twice, as the source and the target sectors are interchangeable, we have

N^{st}_i = Σ_{j≠t} (N^{st}_{ij} + N^{st}_{ji})/2

Then the counting betweenness centrality is

CB_i = [Σ_{s∈V} Σ_{t∈V-(s)} N^{st}(i)] / [n(n-1)]

---

## Page 242

Consider an extra dollar to be used equally randomly in any sector. Then the counting betweenness centrality of any sector reflects the number of times (or the length of the circulation within that sector) that extra dollar would pass through that sector. Thus, this centrality measure will reflect the significance of sectors in amplifying or absorbing the shocks in an economy.

## Section 4: Reconstruction of Input-Output Networks in a Marxian Framework

The reconstruction of I-O networks depends on the distinction between productive and unproductive activities, which is ignored in mainstream economics, and seen as fundamental by Marxian economics. Since available data is in the conventional form, we start reconstructing the existing I-O tables by modifying them as follows.

We first differentiate:

1. **Primary Activities**: Agriculture + Industry + Productive Services.
2. **Secondary Activities**: Trade + Transportation.
3. **Royalties and Government Sectors**: Finance + Real Estate + Public Administration.

Secondary Activities do not contribute to value production but in conventional I-O tables they are treated as if they did. The products of the Primary Activities sectors are transferred to the Secondary Activities sectors at producers' prices and therefore the Secondary Activities sectors seem to sell a service at value of equivalent to the "trade margin" of these sectors. Since in this context as Shaikh and Tonak (1994) argue the total value should reflect total output of both the Primary and the Secondary Activities sectors, we keep them intact under the reconstructed I-O networks.

Recognising the fact that trade entirely and transportation partially are unproductive, we end up including these sectors in our analysis as they are almost impossible to disentangle from input-output tables.

Royalties and Government Sectors, on the other hand, concern mostly the "Revenue Circuit" and are totally non-production activities; so, they are excluded. (i) Public Administration, (ii) Finance, (iii) Real Estate, (iv) Other Business Services and (v) Other community and personal services

---

## Page 243

are the sectors excluded. The resulting symmetric intersectoral value-form flows constitute the basis for our network analysis a la Marxian framework.

Our analysis concerns the Marxian "Productive Capital Circuit" in the sense that inputs and outputs of the production sectors are covered. We should emphasise that within the reconstructed (Marxian) input-output networks, intermediate input flows cover both the value of fixed capital used up and the circulating capital (raw materials and intermediate goods) in value-form quantities.

Reiterating the main difference between the Marxian framework and that of the conventional one, we should say that the distinguishing characteristic of the former is the specification of sectors that are productive in terms of creating value rather than circulating or appropriating it. The elimination of unproductive sectors from the national I-O tables (hence I-O networks) will modify the rankings of the sectors based on centrality measures since some of these unproductive sectors are central in the conventional framework. However, this modification will not affect the sectoral interdependencies among the productive sectors. The application of the complex network analysis on the Marxian I-O networks gives us these modified rankings.

We argue that money flows based on the "values" as in the Marxian I-O networks are more important than the money flows based on "market transactions" as in the conventional I-O networks in specifying the sectors most vulnerable to the global crisis.

After the reconstruction of the I-O networks of three different economies, we present our empirical findings also in graphical forms. The graphical representations of the I-O networks make the interdependencies among sectors visible. Adjusting the vertex (sector) size according to its centrality measures helps one to identify the most vulnerable sectors easily. In return the second-degree vulnerable sectors directly linked to the most vulnerable sectors can be identified readily on the graphs.

## Section 5: Analysis

We begin the analysis focusing on the US economy, the originator of the global crisis. Figure 1 demonstrates the I-O network of the US economy in the mid-2000s. For visibility purposes, as mentioned above, we exclude the edges with less than 3% of the total outflows. The graphs at the bottom of Fig. 1(c) and (d), are the reconstructed networks for the US

---

## Page 244

economy in which the distinction between productive and unproductive economic activities is considered (Figs. 2 and 3).

In Table 1, we rank the sectors in the US economy according to the CB Centrality Measure that we have calculated. Table 1 reflects the fact that in the conventional framework the most central sectors have a stable pattern. Apart from Motor Vehicles and Food sectors the top central sectors are services; more importantly these service sectors are non-tradeable. Moreover, the dominance of the unproductive sectors (Pub. Adm, Real Estate, Other Business Services and Finance) is visible.

[Figure 1 appears here]

---

## Page 245

[Figure 2 appears here]

In Table 2, we carry out the ranking exercise for the new CB measures based on the reconstructed intermediate input network a la Marxian framework. In the Marxian case, the Construction sector moves to the 4th from the 9th place it occupies in the conventional framework.

The difference in top 10 rankings between the conventional and the Marxian case is striking. Almost all the non-production activities (Public Administration., Real Estate, Other Services, etc.) are central in the conventional case. Motor Vehicles and Construction turn out to be much more central in the Marxian case. Relative centrality of Health sector rises

---

## Page 246

[Figure 3 appears here]

dramatically in the Marxian case. Computing Machinery and even R&D become central in the Marxian case.

In Tables 3 and 4 we have the centrality rankings of the sectors derived from the reconstructed I-O networks for Germany in the conventional and Marxian framework, respectively. The rankings in the conventional framework reveal that the central sectors in Germany are mostly productive sectors, although there has been a slight transformation within the 1995-2005 period as Public Administration, Real Estate and Other Business Services sectors joined the top 10 in 2005.

---

## Page 247

[Tables 1, 2, and 3 appear here]

---

## Page 248

[Tables 4 and 5 appear here]

The most important observation for the German economy is the similarity of rankings in both conventional and in Marxian frameworks. The top sectors are largely productive and tradeable sectors.

The Spanish economy is dominated by the Construction sector. As seen in Tables 5 and 6, both in the conventional and in the Marxian framework, the Construction sector is at the top of the rankings by far. The Construction sector as the generic durable goods sector depends on asset prices and expectations. Thus, this sector is one of the most fragile sectors given a global crisis in which consumers downgrade their expectations and asset prices (e.g. house prices) decline.

---

## Footnotes

3. See, https://www.oecd.org/sti/ind/input-outputtables.htm.

4. See, Blöchl, F., Theis, F. J., Vega-Redondo, F., Fisher, E., Vertex Centralities in Input-Output Networks Reveal the Structure of Modern Economies, Physical Review E, 83(4):046127 (2011).
